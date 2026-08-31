import json
import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

from tools import (
    verify_numeric_findings,
    extract_policy_threshold
)

from trajectory_logger import TrajectoryLogger


# ============================================================
# LOCAL OLLAMA CONFIGURATION
# ============================================================

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434"
)

MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen2.5:1.5b"
)


# ============================================================
# JSON EXTRACTION
# ============================================================

def _extract_json(text):
    text = text.strip()

    # Remove markdown code fences if the model added them
    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    try:
        return json.loads(text)

    except json.JSONDecodeError:

        # Try to find the largest JSON object
        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1 and end > start:

            candidate = text[start:end + 1]

            try:
                return json.loads(candidate)

            except json.JSONDecodeError:
                pass

        raise ValueError(
            f"Model did not return valid JSON:\n{text[:1000]}"
        )


# ============================================================
# OLLAMA MODEL CALL
# ============================================================

def call_ollama(instruction, payload):
    """
    Send a request to the local Ollama server.

    No OpenAI API key or paid API is required.
    """

    prompt = f"""
You are an AI agent in the ProcureGuard invoice auditing system.

IMPORTANT:
- Follow the instructions exactly.
- Return ONLY valid JSON.
- Do not use markdown.
- Do not add explanations outside the JSON.
- Do not invent information.
- Use null when information is unavailable.

AGENT INSTRUCTIONS:
{instruction}

INPUT DATA:
{json.dumps(payload, ensure_ascii=False, indent=2)}

Return ONLY the JSON object.
"""

    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0
            }
        },
        timeout=180
    )

    response.raise_for_status()

    data = response.json()

    return data["message"]["content"]


# ============================================================
# GENERIC JSON AGENT
# ============================================================

def call_json_agent(
    name,
    instruction,
    payload,
    logger,
    max_retries=1
):

    for attempt in range(max_retries + 1):

        try:

            text = call_ollama(
                instruction=instruction,
                payload=payload
            )

            result = _extract_json(text)

            logger.log(
                agent=name,
                instruction=instruction,
                input_data=payload,
                action="model_response",
                output=result,
                retry=(attempt > 0),
            )

            return result

        except Exception as exc:

            logger.log(
                agent=name,
                instruction=instruction,
                input_data=payload,
                action="model_error",
                output={"error": str(exc)},
                retry=(attempt > 0),
            )

            if attempt == max_retries:
                raise


# ============================================================
# EXTRACTION AGENT
# ============================================================

def extraction_agent(
    invoice_text,
    po_text,
    policy_text,
    logger
):

    instruction = """
You are the Extraction Agent in an invoice audit workflow.

Extract facts only; do not make the final decision.

Return JSON only.

Use null when a field is unavailable.
Preserve numbers exactly.

Schema:

{
  "invoice": {
    "number": null,
    "vendor": null,
    "po_number": null,
    "currency": null,
    "tax": null,
    "shipping": null,
    "total": null,
    "items": [
      {
        "name": null,
        "quantity": null,
        "unit_price": null
      }
    ]
  },

  "purchase_order": {
    "number": null,
    "vendor": null,
    "currency": null,
    "total": null,
    "items": [
      {
        "name": null,
        "quantity": null,
        "unit_price": null
      }
    ]
  },

  "policy": {
    "variance_threshold_percent": null,
    "rules": []
  }
}
"""

    payload = {
        "invoice_text": invoice_text,
        "purchase_order_text": po_text,
        "policy_text": policy_text
    }

    result = call_json_agent(
        "Extraction Agent",
        instruction,
        payload,
        logger
    )

    # ---------------------------------------------------------
    # Deterministically extract policy threshold.
    # Do not rely on the small LLM for critical policy numbers.
    # ---------------------------------------------------------

    threshold = extract_policy_threshold(
        policy_text
    )

    if threshold is not None:

        result.setdefault(
            "policy",
            {}
        )

        result["policy"][
            "variance_threshold_percent"
        ] = threshold

    return result


# ============================================================
# RECONCILIATION AGENT
# ============================================================

def reconciliation_agent(
    extracted,
    logger
):

    instruction = """
You are the Reconciliation Agent.

Compare invoice facts with purchase-order facts.

Do not invent values.

IMPORTANT:
Only report a discrepancy when the invoice value
and PO value are actually different.

If two values are equal, DO NOT create a finding.

Return JSON only:

{
  "vendor_match": true,
  "po_number_match": true,
  "currency_match": true,
  "line_findings": [
    {
      "type": "...",
      "item": "...",
      "invoice_value": "...",
      "po_value": "...",
      "severity": "low|medium|high"
    }
  ],
  "total_difference": null,
  "summary": "..."
}

Flag only real:

- quantity discrepancies
- unit price discrepancies
- missing items
- extra items
- vendor mismatch
- PO number mismatch
- currency mismatch
- total discrepancies

Do not flag equal values as discrepancies.
"""

    return call_json_agent(
        "Reconciliation Agent",
        instruction,
        {
            "extracted": extracted
        },
        logger
    )


# ============================================================
# POLICY AGENT
# ============================================================

def policy_agent(
    extracted,
    reconciliation,
    logger
):

    instruction = """
You are the Policy Agent.

Determine which policy rules apply to the findings.

Return JSON only:

{
  "applicable_rules": [
    {
      "rule": "...",
      "threshold": "...",
      "result": "pass|violation"
    }
  ],
  "policy_violations": [],
  "required_action": "approve|human_review|reject",
  "summary": "..."
}

Never invent policy rules.

Use only the supplied policy.

IMPORTANT:

- A rule is a violation only when the evidence actually
  satisfies the rule's condition.
- If invoice and PO totals are equal, the variance rule passes.
- If vendor, currency, PO number, quantities and prices match,
  do not report those as violations.
- Duplicate invoices must be rejected only when there is
  actual evidence of duplication.
"""

    payload = {
        "extracted": extracted,
        "reconciliation": reconciliation
    }

    return call_json_agent(
        "Policy Agent",
        instruction,
        payload,
        logger
    )


# ============================================================
# VERIFICATION AGENT
# ============================================================

def verification_agent(
    extracted,
    reconciliation,
    policy,
    logger
):

    invoice = extracted.get(
        "invoice",
        {}
    )

    po = extracted.get(
        "purchase_order",
        {}
    )

    threshold = extracted.get(
        "policy",
        {}
    ).get(
        "variance_threshold_percent"
    )

    # ---------------------------------------------------------
    # IMPORTANT:
    # Financial verification is deterministic Python,
    # not an LLM guess.
    # ---------------------------------------------------------

    numeric_check = verify_numeric_findings(
        invoice.get("total"),
        po.get("total"),
        threshold
    )

    logger.log(
        agent="Verification Agent",
        instruction=(
            "Independently verify important numeric findings "
            "using deterministic calculator tools."
        ),
        input_data={
            "invoice_total": invoice.get("total"),
            "po_total": po.get("total"),
            "threshold": threshold
        },
        action="tool_call",
        tool="verify_numeric_findings",
        tool_input={
            "invoice_total": invoice.get("total"),
            "po_total": po.get("total"),
            "policy_threshold": threshold
        },
        tool_output=numeric_check,
    )

    instruction = """
You are the Verification Agent.

Independently verify the previous findings.

You have a deterministic calculator result.

Do not blindly trust earlier agents.

Return JSON only:

{
  "verified_findings": [],
  "disputed_findings": [],
  "numeric_check": {},
  "verification_status":
      "verified|partially_verified|failed",
  "summary": "..."
}

IMPORTANT:

The deterministic numeric check is authoritative
for invoice total, PO total, variance percentage,
policy threshold and threshold_exceeded.

Do not claim that the threshold was exceeded when
threshold_exceeded is false.
"""

    payload = {
        "extracted": extracted,
        "reconciliation": reconciliation,
        "policy": policy,
        "deterministic_numeric_check": numeric_check
    }

    result = call_json_agent(
        "Verification Agent",
        instruction,
        payload,
        logger
    )

    # Always preserve deterministic result
    result["deterministic_numeric_check"] = numeric_check

    return result


# ============================================================
# DECISION AGENT
# ============================================================

def decision_agent(
    extracted,
    reconciliation,
    policy,
    verification,
    logger
):

    instruction = """
You are the Decision Agent.

Produce a conservative recommendation.

This is NOT an automatic payment action.

Return JSON only:

{
  "decision":
      "APPROVE|HUMAN_REVIEW|REJECT",

  "risk_score": 0,

  "summary": "...",

  "issues": [
    {
      "title": "...",
      "severity": "low|medium|high",
      "evidence": "..."
    }
  ],

  "recommended_action": "..."
}

Use HUMAN_REVIEW when:

- findings are material
- evidence is ambiguous
- agents contradict each other
- policy requires approval

Use APPROVE when there are no genuine discrepancies
and no policy violations.

Use REJECT only when the supplied policy explicitly
requires rejection.

Base the result only on supplied evidence.
"""

    payload = {
        "extracted": extracted,
        "reconciliation": reconciliation,
        "policy": policy,
        "verification": verification
    }

    result = call_json_agent(
        "Decision Agent",
        instruction,
        payload,
        logger
    )

    # ---------------------------------------------------------
    # Deterministic safety guard
    # ---------------------------------------------------------

    numeric_check = verification.get(
        "deterministic_numeric_check",
        {}
    )

    if numeric_check.get(
        "threshold_exceeded"
    ) is True:

        result["decision"] = "HUMAN_REVIEW"

        if result.get(
            "risk_score",
            0
        ) < 50:

            result["risk_score"] = 75

        result["recommended_action"] = (
            "Human review required because the invoice total "
            "exceeds the purchase-order variance threshold."
        )

    # ---------------------------------------------------------
    # If deterministic financial check confirms that the
    # invoice and PO totals match, do not reject based only
    # on a hallucinated variance.
    # ---------------------------------------------------------

    elif (
        numeric_check.get("variance_percent") == 0
        and not numeric_check.get("threshold_exceeded", False)
    ):

        # Only force APPROVE when there are no actual
        # reconciliation findings or policy violations.

        line_findings = reconciliation.get(
            "line_findings",
            []
        )

        vendor_match = reconciliation.get(
            "vendor_match",
            True
        )

        po_number_match = reconciliation.get(
            "po_number_match",
            True
        )

        currency_match = reconciliation.get(
            "currency_match",
            True
        )

        policy_violations = policy.get(
            "policy_violations",
            []
        )

        required_action = str(
            policy.get(
                "required_action",
                ""
            )
        ).lower()

        if (
            not line_findings
            and vendor_match
            and po_number_match
            and currency_match
            and not policy_violations
            and required_action == "approve"
        ):

            result["decision"] = "APPROVE"

            result["risk_score"] = min(
                result.get("risk_score", 0),
                10
            )

            result["recommended_action"] = (
                "Approve. Invoice and purchase order "
                "match and no policy violations were found."
            )

    # ---------------------------------------------------------
    # Human checkpoint
    # ---------------------------------------------------------

    logger.log(
        agent="Decision Agent",
        instruction=instruction,
        input_data=payload,
        action="human_checkpoint",
        output=result,
        human_checkpoint=True,
    )

    return result


# ============================================================
# FULL AGENTIC AUDIT
# ============================================================

def run_audit(
    invoice_text,
    po_text,
    policy_text,
    case_id="live"
):

    logger = TrajectoryLogger(
        case_id=case_id
    )

    extracted = extraction_agent(
        invoice_text,
        po_text,
        policy_text,
        logger
    )

    reconciliation = reconciliation_agent(
        extracted,
        logger
    )

    policy = policy_agent(
        extracted,
        reconciliation,
        logger
    )

    verification = verification_agent(
        extracted,
        reconciliation,
        policy,
        logger
    )

    decision = decision_agent(
        extracted,
        reconciliation,
        policy,
        verification,
        logger
    )

    return {
        "extracted": extracted,
        "reconciliation": reconciliation,
        "policy": policy,
        "verification": verification,
        "decision": decision,
        "trajectory_path":
            str(
                logger.case_dir /
                "trajectory.json"
            )
    }


# ============================================================
# BASELINE
# ============================================================

def run_baseline(
    invoice_text,
    po_text,
    policy_text
):

    instruction = """
You are a basic invoice auditor.

Analyze an invoice, purchase order,
and company policy using ONE general-purpose prompt.

Return JSON only:

{
  "decision":
      "APPROVE|HUMAN_REVIEW|REJECT",

  "issues": [],

  "summary": "..."
}

Do not claim that a payment was executed.

Do not invent evidence.
"""

    payload = {
        "invoice_text": invoice_text,
        "purchase_order_text": po_text,
        "policy_text": policy_text
    }

    text = call_ollama(
        instruction=instruction,
        payload=payload
    )

    return _extract_json(text)