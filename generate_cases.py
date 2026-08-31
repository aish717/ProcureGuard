from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import json

BASE = Path("data/test_cases")
BASE.mkdir(parents=True, exist_ok=True)

def make_pdf(path, title, lines):
    c = canvas.Canvas(str(path), pagesize=A4)
    width, height = A4
    y = height - 60
    c.setFont("Helvetica-Bold", 15)
    c.drawString(50, y, title)
    y -= 30
    c.setFont("Helvetica", 10)
    for line in lines:
        for chunk in [line[i:i+100] for i in range(0, len(line), 100)]:
            c.drawString(50, y, chunk)
            y -= 16
            if y < 50:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 10)
    c.save()

cases = [
    (1, "APPROVE", "No discrepancies."),
    (2, "HUMAN_REVIEW", "Invoice quantity exceeds PO quantity."),
    (3, "HUMAN_REVIEW", "Invoice unit price differs from PO."),
    (4, "HUMAN_REVIEW", "Invoice total is incorrect."),
    (5, "HUMAN_REVIEW", "Tax differs from expected policy."),
    (6, "REJECT", "Duplicate invoice number."),
    (7, "HUMAN_REVIEW", "Purchase order missing."),
    (8, "HUMAN_REVIEW", "Currency mismatch."),
    (9, "HUMAN_REVIEW", "Unexpected shipping fee."),
    (10, "HUMAN_REVIEW", "Policy threshold violated."),
    (11, "APPROVE", "Small variance within policy."),
    (12, "HUMAN_REVIEW", "Vendor mismatch."),
    (13, "HUMAN_REVIEW", "Invoice missing a PO line item."),
    (14, "HUMAN_REVIEW", "Multiple discrepancies."),
    (15, "HUMAN_REVIEW", "Difficult mixed case: quantity and value variance."),
]

for n, expected, note in cases:
    folder = BASE / f"case{n:02d}"
    folder.mkdir(exist_ok=True)

    po_total = 327000
    invoice_total = 327000
    invoice_qty = 5
    po_qty = 5
    if n in {2, 10, 14, 15}:
        invoice_qty = 6
        invoice_total = 387000
    elif n == 3:
        invoice_total = 352000
    elif n == 4:
        invoice_total = 340000
    elif n == 9:
        invoice_total = 337000
    elif n == 11:
        invoice_total = 338000

    po_lines = [
        "PO Number: PO-1042",
        "Vendor: ABC Technologies",
        "Currency: INR",
        "Laptop | Quantity: 5 | Unit Price: 60000",
        "Software License | Quantity: 5 | Unit Price: 5000",
        "Shipping: 2000",
        "PO Total: 327000",
    ]

    invoice_lines = [
        f"Invoice Number: INV-{8800+n}",
        "Vendor: ABC Technologies",
        "PO Number: PO-1042",
        "Currency: INR",
        f"Laptop | Quantity: {invoice_qty} | Unit Price: 60000",
        "Software License | Quantity: 5 | Unit Price: 5000",
        "Shipping: 2000",
        f"Invoice Total: {invoice_total}",
    ]

    policy_lines = [
    "Company Invoice Policy",
    "PO variance above 5 percent requires human approval.",
    "Invoices with duplicate invoice numbers must be rejected.",
    "Missing PO requires human review.",
    "Currency mismatch requires human review.",
    "Tax mismatch between invoice and purchase order requires human review.",
    "Unexpected shipping fee requires human review.",
    "Vendor mismatch requires human review.",
    "Missing invoice line items require human review.",
    ]

    if n == 9:
        invoice_lines = [
            "Shipping: 12000" if x == "Shipping: 2000" else x
            for x in invoice_lines
            ]
    if n == 12:
        invoice_lines[1] = "Vendor: Different Vendor Ltd"
    if n == 6:
        invoice_lines[0] = "Invoice Number: INV-8806"
    invoice_lines.append(
        "Duplicate check: Invoice INV-8806 already exists in the system."
        )
    if n == 7:
        invoice_lines[2] = "PO Number: MISSING"
    if n == 8:
        invoice_lines[3] = "Currency: USD"
    if n == 5:
        invoice_lines.append("Tax: 25000")
        po_lines.append("Expected Tax: 20000")
    if n == 13:
        invoice_lines = [x for x in invoice_lines if "Software License" not in x]
    if n == 14:
        invoice_lines[1] = "Vendor: Different Vendor Ltd"
        invoice_lines[3] = "Currency: USD"

    make_pdf(folder / "purchase_order.pdf", "PURCHASE ORDER", po_lines)
    make_pdf(folder / "invoice.pdf", "INVOICE", invoice_lines)
    make_pdf(folder / "policy.pdf", "COMPANY POLICY", policy_lines)

    expected = {
        "decision": expected,
        "note": note
    }
    (folder / "expected.json").write_text(json.dumps(expected, indent=2), encoding="utf-8")

print(f"Generated {len(cases)} synthetic cases in {BASE}")
