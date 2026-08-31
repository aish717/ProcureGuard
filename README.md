# ProcureGuard — Evidence-First Agentic Invoice Auditor

## 1. Problem

Finance and procurement teams manually compare vendor invoices against purchase
orders and company policies. The work is repetitive and can miss quantity,
price, total, tax, vendor, currency, and policy discrepancies.

## 2. Solution

ProcureGuard is a multi-stage agent workflow that:

1. extracts structured facts from documents,
2. reconciles the invoice against the PO,
3. checks company policy,
4. independently verifies important findings using deterministic calculations,
5. produces an evidence-backed recommendation.

The system recommends `APPROVE`, `HUMAN_REVIEW`, or `REJECT`; it does not execute payments.

## 3. Architecture

Invoice + PO + Policy
-> Extraction Agent
-> Reconciliation Agent
-> Policy Agent
-> Verification Agent
-> Decision Agent
-> Evidence-backed recommendation

## 4. Why the agents are purposeful

- Extraction: converts documents into structured facts.
- Reconciliation: compares invoice and PO.
- Policy: interprets the supplied policy rules.
- Verification: independently checks important findings and calculations.
- Decision: produces a conservative recommendation and evidence.

## 5. Requirements

- Python 3.10–3.14
- OpenAI API key
- Internet connection for model calls

## 6. Setup from a clean environment

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set:

```text
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-5
```

Use a model available to your API project. The application reads `OPENAI_MODEL`
from the environment.

## 7. Generate synthetic evaluation data

```powershell
python generate_cases.py
```

This creates 15 synthetic invoice/PO/policy cases under `data/test_cases/`.

## 8. Run the application

```powershell
streamlit run app.py
```

Open the local URL shown by Streamlit, normally `http://localhost:8501`.

Upload:
- invoice.pdf
- purchase_order.pdf
- policy.pdf

Click `Run Audit`.

## 9. Run the baseline

```powershell
python evaluator.py --mode baseline --limit 15
```

## 10. Run the final agent workflow

```powershell
python evaluator.py --mode final --limit 15
```

## 11. Run both

```powershell
python evaluator.py --mode both --limit 15
```

Results are written to:

```text
evaluation/results.csv
```

Representative trajectories are written to:

```text
trajectories/caseXX/trajectory.json
```

## 12. Expected output

The UI should produce:
- decision,
- risk score,
- issues,
- evidence,
- deterministic verification result,
- recommendation,
- expandable agent trajectories.

## 13. Evaluation

The baseline and final system should be evaluated on the same fixed cases.
Primary metric: decision accuracy.

Secondary metrics:
- runtime per case,
- estimated model cost,
- failure cases.

Do not claim improvement until the evaluation has actually been run.

## 14. Improvement Changelog

See `CHANGELOG.md`. Each meaningful iteration should record:
- what changed,
- why it was tried,
- evidence/result,
- keep/revise/remove decision.

## 15. Agent Trajectories

See `trajectories/`. Each representative trajectory records:
- agent,
- instruction,
- input,
- action,
- tool,
- tool output,
- model output,
- retry flag,
- human checkpoint.

## 16. Safety

ProcureGuard only recommends a decision. Payment or other consequential actions
remain under authorized human control.

## 17. Reproducibility

Synthetic data is generated locally by `generate_cases.py`, so no private
customer information is required.

## 18. Main failure mode

The current prototype relies on text extraction and model interpretation.
Scanned/image-only PDFs, ambiguous documents, or unusual policy wording can
reduce reliability. These should be included in failure analysis rather than hidden.

## 19. Hot take

The final hot take must be based on measured experiments. A candidate hypothesis
to test is that independent verification improves reliability more than simply
adding another reasoning agent.

## 20. Approximate cost

API cost depends on the model selected, document length, and number of agent calls.
Record the actual usage/cost from the evaluation run rather than inventing a number.
