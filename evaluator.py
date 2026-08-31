import argparse
import csv
import json
import os
import time
from pathlib import Path
from dotenv import load_dotenv

from pdf_utils import extract_pdf_text
from agents import run_baseline, run_audit

load_dotenv()

def load_case(folder):
    invoice = extract_pdf_text((folder / "invoice.pdf").read_bytes())
    po = extract_pdf_text((folder / "purchase_order.pdf").read_bytes())
    policy = extract_pdf_text((folder / "policy.pdf").read_bytes())
    expected = json.loads((folder / "expected.json").read_text(encoding="utf-8"))
    return invoice, po, policy, expected

def normalize(decision):
    return str(decision).upper().replace(" ", "_")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["baseline", "final", "both"], default="both")
    parser.add_argument("--limit", type=int, default=15)
    args = parser.parse_args()

    base = Path("data/test_cases")
    folders = sorted(base.glob("case*"))[:args.limit]
    out = Path("evaluation")
    out.mkdir(exist_ok=True)

    rows = []
    for folder in folders:
        invoice, po, policy, expected = load_case(folder)
        expected_decision = normalize(expected["decision"])

        baseline_decision = ""
        baseline_time = ""
        final_decision = ""
        final_time = ""

        if args.mode in {"baseline", "both"}:
            start = time.perf_counter()
            b = run_baseline(invoice, po, policy)
            baseline_time = round(time.perf_counter() - start, 3)
            baseline_decision = normalize(b.get("decision", ""))

        if args.mode in {"final", "both"}:
            start = time.perf_counter()
            f = run_audit(invoice, po, policy, case_id=folder.name)
            final_time = round(time.perf_counter() - start, 3)
            final_decision = normalize(f["decision"].get("decision", ""))

        rows.append({
            "case_id": folder.name,
            "expected": expected_decision,
            "baseline": baseline_decision,
            "final": final_decision,
            "baseline_correct": bool(baseline_decision and baseline_decision == expected_decision),
            "final_correct": bool(final_decision and final_decision == expected_decision),
            "baseline_time_sec": baseline_time,
            "final_time_sec": final_time,
        })

    path = out / "results.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {path}")
    if rows:
        b_count = sum(r["baseline_correct"] for r in rows)
        f_count = sum(r["final_correct"] for r in rows)
        print(f"Baseline accuracy: {b_count/len(rows)*100:.1f}%")
        print(f"Final accuracy:    {f_count/len(rows)*100:.1f}%")

if __name__ == "__main__":
    main()
