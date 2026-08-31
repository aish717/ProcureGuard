# Improvement Changelog

> Fill the result numbers only after running the corresponding experiment.

## Baseline — Single general-purpose prompt
- **Why:** Establish a simple, credible comparison point.
- **Change:** Invoice + PO + policy sent to one auditor prompt.
- **Evidence:** `evaluation/results.csv`
- **Decision:** Starting point.

## Iteration 1 — Structured extraction
- **Why:** Reduce repeated interpretation of raw document text.
- **Change:** Added Extraction Agent.
- **Evidence:** Record baseline vs extraction accuracy.
- **Decision:** Keep/revise/remove based on results.

## Iteration 2 — Reconciliation
- **Why:** Make invoice/PO comparison explicit.
- **Change:** Added Reconciliation Agent.
- **Evidence:** Record accuracy and failure cases.
- **Decision:** Keep/revise/remove.

## Iteration 3 — Policy reasoning
- **Why:** Separate factual reconciliation from policy interpretation.
- **Change:** Added Policy Agent.
- **Evidence:** Record policy-case accuracy.
- **Decision:** Keep/revise/remove.

## Iteration 4 — Independent verification
- **Why:** Check important calculations and findings before the final recommendation.
- **Change:** Added Verification Agent plus deterministic calculator tools.
- **Evidence:** Record accuracy and difficult-case behavior.
- **Decision:** Keep/revise/remove.

## Iteration 5 — Extra risk agent
- **Why:** Test whether another reasoning agent adds useful signal.
- **Change:** Temporary additional risk-analysis stage.
- **Evidence:** Compare accuracy, latency and cost.
- **Decision:** Remove if it does not produce meaningful improvement.

## Final
- Combine only the components supported by the evaluation evidence.
- Report actual measured accuracy, runtime and cost.
