\# Changelog



All notable changes to ProcureGuard are documented here.



\## \[1.0.0] - 2026-08-31



\### Added



\- Multi-agent invoice audit workflow

\- PDF invoice, purchase order, and policy extraction

\- Invoice and PO reconciliation

\- Policy compliance checking

\- Deterministic numeric verification

\- Decision Agent with `APPROVE`, `HUMAN\_REVIEW`, and `REJECT` recommendations

\- Human-in-the-loop checkpoint

\- Audit trajectory logging

\- Streamlit user interface

\- Local Ollama / Qwen 2.5 1.5B integration

\- Synthetic dataset with 15 invoice-audit cases

\- Baseline vs. ProcureGuard evaluation

\- Evaluation documentation and project structure



\### Safety



\- No automatic payment execution

\- Conservative human-review recommendations for ambiguous or material findings

\- Important financial calculations verified deterministically



\### Evaluation



\- Added 15 synthetic test cases

\- Added baseline comparison

\- Current benchmark:

&#x20; - Baseline accuracy: 6.7%

&#x20; - ProcureGuard accuracy: 46.7%



\### Documentation



\- Added project README

\- Added project plan

\- Added setup and usage instructions

\- Added evaluation documentation

