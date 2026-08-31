# ProcureGuard

## AI-Powered Multi-Agent Invoice Audit System

ProcureGuard is an AI-assisted invoice auditing system that compares invoices with purchase orders and company policies to identify discrepancies and provide a recommendation.



> \*\*Note:\*\* ProcureGuard provides recommendations only and does not automatically execute payments.


---

## ✨ Features



- 📄 PDF invoice, PO, and policy processing

- 🤖 Multi-agent audit workflow

- 🔍 Invoice and purchase-order reconciliation

- 📋 Policy compliance checking

- 🧮 Deterministic numeric verification

- 🧑‍💼 Human-in-the-loop decision checkpoint

- 📝 Audit trajectory logging

- 📊 Baseline vs. ProcureGuard evaluation

- 🖥️ Streamlit interface

- 🏠 Local LLM inference with Ollama



---

## 🔄 Workflow



```text

Invoice + Purchase Order + Policy

               ↓

       Document Extraction

               ↓

       Extraction Agent

               ↓

     Reconciliation Agent

               ↓

         Policy Agent

               ↓

      Verification Agent

               ↓

        Decision Agent

               ↓

        Human Review

               ↓

         Recommendation

