# ProcureGuard

## AI-Powered Multi-Agent Invoice Audit System

ProcureGuard is an AI-assisted invoice auditing system designed to analyze invoices against purchase orders and company policies.


The system uses a structured multi-agent workflow to extract information from business documents, reconcile invoice data against purchase-order data, evaluate policy compliance, independently verify important numeric findings, and generate a conservative recommendation for an authorized human reviewer.


> \*\*Important:\*\* ProcureGuard provides recommendations only. It does not execute payments or make autonomous consequential financial decisions.

---

## Table of Contents

- \[Overview](#overview)

- \[Problem Statement](#problem-statement)

- \[Solution](#solution)

- \[Key Features](#key-features)

- \[System Architecture](#system-architecture)

- \[Multi-Agent Workflow](#multi-agent-workflow)

- \[Agent Responsibilities](#agent-responsibilities)

- \[Deterministic Verification](#deterministic-verification)

- \[Human-in-the-Loop](#human-in-the-loop)

\- \[Technology Stack](#technology-stack)

\- \[Project Structure](#project-structure)

\- \[Prerequisites](#prerequisites)

\- \[Installation](#installation)

\- \[Configuration](#configuration)

\- \[Running the Application](#running-the-application)

\- \[Using ProcureGuard](#using-procureguard)

\- \[Test Dataset](#test-dataset)

\- \[Evaluation](#evaluation)

\- \[Evaluation Results](#evaluation-results)

\- \[Audit Trajectory Logging](#audit-trajectory-logging)

\- \[Safety and Reliability](#safety-and-reliability)

\- \[Limitations](#limitations)

\- \[Future Improvements](#future-improvements)

\- \[Demo](#demo)

\- \[Submission](#submission)

\- \[Disclaimer](#disclaimer)



\---



\# Overview



Invoice auditing often requires reviewing several related documents and checking whether the information contained in them is consistent.



A typical audit may require comparing:



\- Invoice number

\- Vendor name

\- Purchase-order number

\- Currency

\- Product or service names

\- Quantities

\- Unit prices

\- Taxes

\- Shipping charges

\- Invoice totals

\- Purchase-order totals

\- Company policy requirements



ProcureGuard demonstrates an AI-assisted approach to this process using multiple specialized agents rather than relying on one general-purpose model prompt.



The system combines:



1\. Document extraction

2\. Invoice and PO reconciliation

3\. Policy evaluation

4\. Deterministic numeric verification

5\. AI-based reasoning

6\. Conservative decision recommendation

7\. Human review



\---



\# Problem Statement



Manual invoice auditing can be repetitive and time-consuming because information must be gathered from multiple documents and compared carefully.



For example, an auditor may need to determine:



\- Does the invoice belong to the correct vendor?

\- Does the invoice reference the correct purchase order?

\- Are the quantities the same?

\- Are unit prices the same?

\- Are there missing or unexpected items?

\- Is the currency correct?

\- Is the invoice total consistent with the purchase order?

\- Does the variance exceed the company policy threshold?

\- Does a special policy rule require human review?

\- Should the invoice be approved, reviewed, or rejected?



Errors in these comparisons can result in incorrect recommendations.



ProcureGuard is designed as a prototype demonstrating how AI agents and deterministic validation can work together to assist with this process.



\---



\# Solution



ProcureGuard accepts three PDF documents:



1\. Invoice

2\. Purchase Order

3\. Company Policy



The documents are converted into text and processed through a sequence of specialized agents.



The agents have separate responsibilities so that extraction, reconciliation, policy interpretation, verification, and final recommendation are handled as distinct stages.



The system also uses deterministic Python functions for important financial calculations.



\---



\# Key Features



\### Document Processing



\- PDF document input

\- Invoice text extraction

\- Purchase-order text extraction

\- Policy text extraction



\### Multi-Agent Processing



\- Extraction Agent

\- Reconciliation Agent

\- Policy Agent

\- Verification Agent

\- Decision Agent



\### Invoice Audit Checks



\- Vendor matching

\- PO-number matching

\- Currency matching

\- Quantity comparison

\- Unit-price comparison

\- Missing line-item detection

\- Extra line-item detection

\- Invoice total comparison

\- PO variance calculation

\- Tax comparison

\- Shipping comparison

\- Policy-rule evaluation



\### Verification



\- Deterministic percentage-variance calculation

\- Deterministic threshold comparison

\- Independent verification stage

\- Protection against relying entirely on model arithmetic



\### Decision Support



The system produces one of three recommendations:



```text

APPROVE

HUMAN\_REVIEW

REJECT

Governance

Human-in-the-loop checkpoint

Audit trajectory logging

Evidence-based recommendation

No automatic payment execution

System Architecture

&#x20;                        INPUT DOCUMENTS

&#x20;                             |

&#x20;            +----------------+----------------+

&#x20;            |                |                |

&#x20;            v                v                v

&#x20;       Invoice PDF      Purchase Order     Policy PDF

&#x20;                             |

&#x20;                             v

&#x20;                   +--------------------+

&#x20;                   |   PDF Extraction   |

&#x20;                   +---------+----------+

&#x20;                             |

&#x20;                             v

&#x20;                   +--------------------+

&#x20;                   |  Extraction Agent  |

&#x20;                   +---------+----------+

&#x20;                             |

&#x20;                             v

&#x20;                 +------------------------+

&#x20;                 | Reconciliation Agent   |

&#x20;                 +-----------+------------+

&#x20;                             |

&#x20;                             v

&#x20;                   +--------------------+

&#x20;                   |    Policy Agent    |

&#x20;                   +---------+----------+

&#x20;                             |

&#x20;                             v

&#x20;                 +------------------------+

&#x20;                 |   Verification Agent   |

&#x20;                 |                        |

&#x20;                 | Deterministic Python   |

&#x20;                 | Numeric Verification   |

&#x20;                 +-----------+------------+

&#x20;                             |

&#x20;                             v

&#x20;                   +--------------------+

&#x20;                   |   Decision Agent   |

&#x20;                   +---------+----------+

&#x20;                             |

&#x20;                             v

&#x20;                   +--------------------+

&#x20;                   | Human Checkpoint   |

&#x20;                   +---------+----------+

&#x20;                             |

&#x20;                             v

&#x20;                      Recommendation

Multi-Agent Workflow

Stage 1 — Document Extraction



The input PDFs are processed and converted into text.



The extracted text is provided to the Extraction Agent.



Stage 2 — Extraction Agent



The Extraction Agent identifies structured information from the supplied documents.



Invoice Information



Examples include:



Invoice number

Vendor

PO number

Currency

Tax

Shipping

Total

Line items

Quantity

Unit price

Purchase-Order Information



Examples include:



PO number

Vendor

Currency

Total

Line items

Quantity

Unit price

Policy Information



Examples include:



Variance threshold

Applicable policy rules



The extraction stage is focused on identifying facts rather than making the final decision.



Stage 3 — Reconciliation Agent



The Reconciliation Agent compares extracted invoice information with purchase-order information.



The comparison includes:



Vendor

Invoice Vendor

&#x20;      vs.

PO Vendor

Purchase Order Number

Invoice PO Number

&#x20;      vs.

PO Number

Currency

Invoice Currency

&#x20;      vs.

PO Currency

Quantity

Invoice Quantity

&#x20;      vs.

PO Quantity

Unit Price

Invoice Unit Price

&#x20;      vs.

PO Unit Price

Line Items



The agent checks for:



Missing items

Extra items

Different item information

Total



The invoice total is compared against the purchase-order total.



The reconciliation stage is instructed to report genuine discrepancies rather than treating equal values as discrepancies.



Stage 4 — Policy Agent



The Policy Agent determines which supplied company policies apply to the identified findings.



The synthetic test policies include rules such as:



PO variance above 5 percent requires human approval.



Invoices with duplicate invoice numbers must be rejected.



Missing PO requires human review.



Currency mismatch requires human review.



The Policy Agent uses the supplied policy rather than inventing new policy requirements.



Stage 5 — Verification Agent



The Verification Agent independently checks important findings.



A deterministic Python verification layer is used for important numeric calculations.



For example:



Invoice Total

&#x20;     |

&#x20;     v

PO Total

&#x20;     |

&#x20;     v

Percentage Variance

&#x20;     |

&#x20;     v

Policy Threshold

&#x20;     |

&#x20;     v

Threshold Exceeded?



This separates financial arithmetic from language-model reasoning.



Deterministic Verification



ProcureGuard includes Python functions for deterministic financial calculations.



Examples include:



Percentage Difference

absolute(invoice\_total - po\_total)

\------------------------------------ × 100

&#x20;         absolute(po\_total)

Line Total

quantity × unit price

Policy Threshold



The system can deterministically extract and compare the policy variance threshold.



For example:



Invoice Total = ₹327,000

PO Total      = ₹327,000



Variance      = 0%



Policy Limit  = 5%



Threshold exceeded = False



This provides an additional reliability layer instead of asking the language model to perform all financial calculations itself.



Stage 6 — Decision Agent



The Decision Agent produces a conservative recommendation based on:



Extracted document information

Reconciliation findings

Policy results

Verification results

Deterministic numeric checks



The available decisions are:



APPROVE



Used when the available evidence indicates that the invoice matches the purchase order and no applicable policy violation requires review.



HUMAN\_REVIEW



Used when:



Findings are material

Evidence is ambiguous

Agents contradict one another

A policy requires human approval

Important information is missing

A significant discrepancy is detected

REJECT



Used when the supplied policy explicitly requires rejection, such as a confirmed duplicate invoice.



Human-in-the-Loop



ProcureGuard is designed as a decision-support system rather than an autonomous payment system.



The final recommendation is not an automatic payment action.



An authorized human reviewer remains responsible for the final consequential decision.



The workflow can therefore be represented as:



AI Analysis

&#x20;    |

&#x20;    v

Verification

&#x20;    |

&#x20;    v

Recommendation

&#x20;    |

&#x20;    v

Human Review

&#x20;    |

&#x20;    v

Final Authorized Action



This design helps keep human oversight in the workflow.



Technology Stack

Technology	Purpose

Python	Core application and agent workflow

Streamlit	Web-based user interface

Ollama	Local LLM inference

Qwen 2.5 1.5B	Local language model

Requests	Communication with Ollama API

PyMuPDF	PDF text extraction

ReportLab	Synthetic PDF test generation

JSON	Structured agent output

CSV	Evaluation results

PowerShell	Windows development environment

Git	Version control

GitHub	Source-code hosting

Local LLM



ProcureGuard uses Ollama for local inference.



The configured model is:



qwen2.5:1.5b



Running the model locally provides a way to demonstrate the project without requiring a hosted LLM API.



The model is used for agent reasoning and structured output generation.



Deterministic Python functions are used for important numeric verification.



Project Structure

ProcureGuard/

|

+-- agents.py

|     Multi-agent workflow and local Ollama integration

|

+-- app.py

|     Streamlit application

|

+-- tools.py

|     Deterministic financial verification functions

|

+-- evaluator.py

|     Baseline and multi-agent evaluation

|

+-- generate\_cases.py

|     Synthetic test-case generator

|

+-- pdf\_utils.py

|     PDF text extraction utilities

|

+-- trajectory\_logger.py

|     Agent trajectory and audit logging

|

+-- smoke\_test.py

|     Basic application checks

|

+-- requirements.txt

|     Python dependencies

|

+-- README.md

|     Project documentation

|

+-- CHANGELOG.md

|     Project change history

|

+-- PROJECT\_PLAN.md

|     Project planning information

|

+-- data/

|   |

|   +-- test\_cases/

|       +-- case01/

|       +-- case02/

|       +-- ...

|       +-- case15/

|

+-- evaluation/

|   +-- evaluation\_report.md

|

+-- trajectories/

&#x20;   +-- .gitkeep

Prerequisites



Before running ProcureGuard, install:



Python 3.11 or compatible version

Ollama

Git (optional for development)



The application was developed and tested on Windows using PowerShell.



Installation

1\. Install Python



Install Python 3.11 or a compatible version.



Verify the installation:



python --version

2\. Install Ollama



Install Ollama and make sure the Ollama service is running.



Verify Ollama:



ollama --version

3\. Download the Model



Pull the configured model:



ollama pull qwen2.5:1.5b



Verify that it is installed:



ollama list



The model should appear as:



qwen2.5:1.5b

Python Environment Setup



Create a virtual environment:



python -m venv .venv



Activate it:



.\\.venv\\Scripts\\Activate.ps1



If PowerShell blocks script execution for the current session, use:



Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned



Then activate:



.\\.venv\\Scripts\\Activate.ps1

Install Python Dependencies



Run:



pip install -r requirements.txt

Configuration



Create a .env file in the project root.



Example:



OLLAMA\_URL=http://localhost:11434

OLLAMA\_MODEL=qwen2.5:1.5b



The .env file is intentionally excluded from Git version control.



Do not commit API keys, passwords, tokens, or other secrets to the repository.



Running Ollama



Ollama normally provides a local server at:



http://localhost:11434



If the Ollama service is not already running, start it:



ollama serve



If you receive an error indicating that port 11434 is already in use, Ollama is likely already running.



In that situation, do not start another Ollama server.



You can verify the service with:



Invoke-RestMethod http://localhost:11434/api/tags



The installed model should be listed.



Running the Streamlit Application



From the ProcureGuard project directory:



python -m streamlit run app.py



The application will open in a browser.



The default Streamlit address is typically:



http://localhost:8501

Using ProcureGuard

Step 1 — Open the Application



Start Streamlit:



python -m streamlit run app.py



Open the displayed local URL in a browser.



Step 2 — Upload Documents



Upload:



Invoice PDF

Purchase Order PDF

Company Policy PDF



The project includes synthetic test documents under:



data/test\_cases/



Each test case contains:



invoice.pdf

purchase\_order.pdf

policy.pdf

expected.json

Step 3 — Run the Audit



Start the audit workflow.



ProcureGuard processes the case through the agent stages:



01 Extracting documents



02 Reconciling invoice against purchase order



03 Checking policy



04 Independently verifying findings



05 Generating recommendation

Step 4 — Review Results



The application generates a recommendation:



APPROVE



or:



HUMAN\_REVIEW



or:



REJECT



The recommendation is supported by findings and verification information.



Test Dataset



ProcureGuard includes 15 synthetic invoice-audit test cases.



The test cases are generated by:



generate\_cases.py



The cases cover different audit scenarios.



Case	Scenario	Expected Decision

01	No discrepancies	APPROVE

02	Invoice quantity exceeds PO quantity	HUMAN\_REVIEW

03	Invoice unit price differs from PO	HUMAN\_REVIEW

04	Invoice total discrepancy	HUMAN\_REVIEW

05	Tax mismatch	HUMAN\_REVIEW

06	Duplicate invoice	REJECT

07	Missing PO	HUMAN\_REVIEW

08	Currency mismatch	HUMAN\_REVIEW

09	Unexpected shipping fee	HUMAN\_REVIEW

10	Policy threshold violation	HUMAN\_REVIEW

11	Small variance within policy	APPROVE

12	Vendor mismatch	HUMAN\_REVIEW

13	Missing invoice line item	HUMAN\_REVIEW

14	Multiple discrepancies	HUMAN\_REVIEW

15	Mixed quantity and value variance	HUMAN\_REVIEW



The dataset is synthetic and is intended for demonstration and evaluation purposes.



Generating Test Cases



To regenerate the synthetic test cases:



python generate\_cases.py



The generated files are stored under:



data/test\_cases/

Evaluation



The project includes an evaluation framework that compares:



Baseline



A basic single-prompt invoice auditing approach.



ProcureGuard



The multi-agent workflow consisting of:



Extraction

&#x20;    ↓

Reconciliation

&#x20;    ↓

Policy

&#x20;    ↓

Verification

&#x20;    ↓

Decision

Running the Evaluation



To run both the baseline and final multi-agent system:



python evaluator.py --mode both --limit 15



For a quick test, use a smaller limit:



python evaluator.py --mode both --limit 2



The generated results are stored locally in:



evaluation/results.csv



This generated file is excluded from version control.



Evaluation Results



The current 15-case synthetic benchmark produced:



Metric	Result

Number of test cases	15

Baseline accuracy	6.7%

ProcureGuard accuracy	46.7%

Improvement	+40.0 percentage points



The multi-agent workflow therefore performed better than the implemented single-prompt baseline on the current synthetic benchmark.



Note: This is a small synthetic benchmark and should not be interpreted as production-level accuracy.



A larger, more diverse, independently validated dataset would be required for meaningful production evaluation.



Audit Trajectory Logging



ProcureGuard records the execution trajectory of the multi-agent workflow.



Trajectory information can include:



Agent name

Agent instructions

Input data

Model response

Tool calls

Verification results

Errors

Retry information

Human checkpoint information



This provides visibility into how the audit recommendation was generated.



Generated trajectory files are intentionally excluded from Git version control because they are runtime artifacts.



Safety and Reliability



ProcureGuard is designed to separate AI reasoning from deterministic validation where possible.



Deterministic Numeric Verification



Important financial calculations are performed by Python functions rather than relying entirely on the language model.



Examples include:



Invoice total comparison

PO total comparison

Percentage variance

Policy threshold comparison

Line-total calculations

Conservative Recommendations



The Decision Agent is instructed to use:



HUMAN\_REVIEW



when findings are material, ambiguous, contradictory, or require human approval.



Human Oversight



ProcureGuard does not automatically execute payments.



The system provides a recommendation that an authorized human reviewer can evaluate before taking consequential action.



Why Use Multiple Agents?



A single general-purpose prompt can combine document extraction, reconciliation, policy interpretation, verification, and decision-making into one step.



ProcureGuard separates these responsibilities.



This provides a structured workflow:



Extraction

&#x20;  ↓

Comparison

&#x20;  ↓

Policy Evaluation

&#x20;  ↓

Independent Verification

&#x20;  ↓

Decision



The separation makes it easier to:



Identify errors

Inspect intermediate results

Add deterministic checks

Log agent behavior

Improve individual stages

Maintain human oversight

Baseline Comparison



The project includes a basic baseline auditor for comparison.



The baseline uses a single general-purpose prompt to analyze the invoice, purchase order, and policy.



ProcureGuard instead uses multiple specialized stages.



The benchmark is designed to demonstrate the difference between these approaches on the included synthetic dataset.



Limitations



ProcureGuard is a prototype and has several limitations.



Dataset



The evaluation dataset contains only 15 synthetic cases.



It does not represent the full variety of real-world invoices.



Language Model



The project uses the local Qwen 2.5 1.5B model.



A relatively small local model may produce inconsistent results on complex or ambiguous cases.



Performance



Local model inference can be slow depending on available CPU, GPU, RAM, and storage.



Document Complexity



The current prototype primarily targets text-based PDF documents.



Real-world invoices may contain:



Scanned pages

Images

Tables

Handwritten information

Complex layouts

Poor-quality OCR

Multiple currencies

Multiple tax structures

Duplicate Detection



A production implementation would require integration with an invoice history database or enterprise system to reliably identify previously processed invoices.



Production Security



A production system would require additional:



Authentication

Authorization

Encryption

Monitoring

Audit controls

Data-retention policies

Compliance controls

Error handling

Access controls

Future Improvements



Potential improvements include:



Better Document Processing

OCR for scanned invoices

Table-aware PDF extraction

Image-based document understanding

Improved structured extraction

Better AI Reasoning

Larger local models

Specialized financial models

Better structured-output validation

Confidence scoring

More robust ambiguity handling

Enterprise Integration

ERP integration

Procurement-system integration

Invoice databases

Vendor databases

Purchase-order APIs

Security

Authentication

Role-based access control

Secure document storage

Encryption

Audit trails

Data retention controls

Evaluation

Larger datasets

Real-world invoice samples

More edge cases

Human-validated labels

Precision/recall metrics

Per-case error analysis

Performance benchmarking

User Experience

Improved dashboards

Review queues

Reviewer comments

Exportable audit reports

Searchable audit history

Notification workflows

Demo



A demonstration video accompanies the project submission.



The demo demonstrates the complete workflow:



Document Upload

&#x20;     ↓

Document Extraction

&#x20;     ↓

Invoice/PO Reconciliation

&#x20;     ↓

Policy Checking

&#x20;     ↓

Independent Verification

&#x20;     ↓

Decision Recommendation

&#x20;     ↓

Human Checkpoint



The video is intended to demonstrate the application workflow and major functionality.



Submission



The project submission contains:



ProcureGuard/

|

+-- Source Code

+-- Configuration Example

+-- Synthetic Test Cases

+-- Evaluation Documentation

+-- Project Documentation



The submission package should not contain:



.env

.venv/

\_\_pycache\_\_/

\*.pyc

evaluation/results.csv

runtime trajectory files



These files are excluded through .gitignore.



A separate demonstration video accompanies the project submission.



GitHub Repository



Source code and documentation:



https://github.com/aish717/ProcureGuard



Quick Start



For a quick local setup:



git clone https://github.com/aish717/ProcureGuard.git

cd ProcureGuard



python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1



pip install -r requirements.txt



ollama pull qwen2.5:1.5b



Create .env:



OLLAMA\_URL=http://localhost:11434

OLLAMA\_MODEL=qwen2.5:1.5b



Then start the application:



python -m streamlit run app.py

Project Status



Current status:



Prototype / Demonstration



Implemented:



PDF document processing

Multi-agent invoice audit workflow

Local Ollama inference

Qwen 2.5 1.5B integration

Invoice/PO reconciliation

Policy evaluation

Deterministic numeric verification

Decision recommendation

Human checkpoint

Trajectory logging

Synthetic evaluation dataset

Baseline comparison

Streamlit interface

Disclaimer



ProcureGuard is an educational and prototype system demonstrating AI-assisted invoice auditing.



It is not intended to independently make financial decisions, execute payments, or replace authorized human review.



Production deployment would require extensive validation, security controls, compliance review, monitoring, and testing using appropriate real-world data.

