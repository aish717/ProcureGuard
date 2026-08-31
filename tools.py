import re


def safe_float(value):
    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    try:
        text = str(value).strip()

        if not text:
            return None

        text = text.replace("₹", "")
        text = text.replace("$", "")
        text = text.replace("€", "")
        text = text.replace("£", "")

        text = re.sub(
            r"\b(INR|USD|EUR|GBP|Rs\.?)\b",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = text.replace(",", "")
        text = text.replace("%", "")

        match = re.search(r"-?\d+(?:\.\d+)?", text)

        if not match:
            return None

        return float(match.group(0))

    except (TypeError, ValueError):
        return None


def extract_policy_threshold(policy_text):
    """
    Deterministically extract the PO variance threshold
    from the supplied company policy.
    """

    if not policy_text:
        return None

    patterns = [
        r"variance\s+above\s+(\d+(?:\.\d+)?)\s*percent",
        r"variance\s+above\s+(\d+(?:\.\d+)?)\s*%",
        r"variance\s+(?:threshold|limit)\s*(?:is|of)?\s*(\d+(?:\.\d+)?)\s*%",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            policy_text,
            flags=re.IGNORECASE
        )

        if match:
            return float(match.group(1))

    return None


def calculate_percentage_difference(invoice_total, po_total):
    invoice = safe_float(invoice_total)
    po = safe_float(po_total)

    if invoice is None or po is None or po == 0:
        return None

    return round(
        abs(invoice - po) / abs(po) * 100,
        2
    )


def calculate_line_total(quantity, unit_price):
    q = safe_float(quantity)
    p = safe_float(unit_price)

    if q is None or p is None:
        return None

    return round(q * p, 2)


def verify_numeric_findings(
    invoice_total,
    po_total,
    policy_threshold
):
    variance = calculate_percentage_difference(
        invoice_total,
        po_total
    )

    threshold = safe_float(policy_threshold)

    return {
        "invoice_total": invoice_total,
        "po_total": po_total,
        "variance_percent": variance,
        "policy_threshold_percent": threshold,
        "threshold_exceeded": (
            variance is not None
            and threshold is not None
            and variance > threshold
        ),
    }