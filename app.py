import os
import json
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
from pdf_utils import extract_pdf_text
from agents import run_audit

load_dotenv()

st.set_page_config(
    page_title="ProcureGuard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    .stApp { background: #f7f8fa; }
    .block-container { max-width: 1180px; padding-top: 2rem; }
    .brand { font-size: 1.55rem; font-weight: 800; letter-spacing: -0.03em; }
    .muted { color: #667085; }
    .hero { padding: 2rem 0 1rem 0; }
    .hero h1 { font-size: 3rem; line-height: 1.0; letter-spacing: -0.05em; margin-bottom: .7rem; }
    .hero p { font-size: 1.05rem; color: #667085; max-width: 680px; }
    .status { display:inline-block; padding:.35rem .7rem; border-radius:999px;
              background:#ecfdf3; color:#027a48; font-size:.82rem; font-weight:700; }
    .card { background:white; border:1px solid #eaecf0; border-radius:18px; padding:1.2rem; }
    .result { background:white; border:1px solid #eaecf0; border-radius:20px; padding:1.5rem; }
    .decision { font-size:1.8rem; font-weight:800; letter-spacing:-.03em; }
    .metric { background:#f9fafb; border:1px solid #eaecf0; border-radius:14px; padding:1rem; }
    .small { color:#667085; font-size:.82rem; }
    div[data-testid="stFileUploader"] { background:white; border-radius:16px; }
    .stButton > button { border-radius:12px; font-weight:700; min-height:3rem; }
</style>
""", unsafe_allow_html=True)

if "audit_result" not in st.session_state:
    st.session_state.audit_result = None

st.markdown(
    '<div class="brand">🛡️ ProcureGuard <span class="status">● System Ready</span></div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="hero">
<h1>Audit invoices<br>with confidence.</h1>
<p>AI checks the documents. Independent verification checks the AI.
Get an evidence-backed recommendation before a consequential payment decision.</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    invoice = st.file_uploader("Invoice", type=["pdf"], key="invoice")
with c2:
    po = st.file_uploader("Purchase Order", type=["pdf"], key="po")
with c3:
    policy = st.file_uploader("Company Policy", type=["pdf"], key="policy")

ready = invoice is not None and po is not None and policy is not None

st.write("")
if st.button("✦  Run Audit", type="primary", use_container_width=True, disabled=not ready):
    with st.status("Agents are working...", expanded=True) as status:
        st.write("01  Extracting documents")
        invoice_text = extract_pdf_text(invoice.getvalue())
        po_text = extract_pdf_text(po.getvalue())
        policy_text = extract_pdf_text(policy.getvalue())

        st.write("02  Reconciling invoice against purchase order")
        st.write("03  Checking policy")
        st.write("04  Independently verifying findings")
        st.write("05  Generating recommendation")

        try:
            result = run_audit(
                invoice_text, po_text, policy_text,
                case_id="live"
            )
            st.session_state.audit_result = result
            status.update(label="✓ Audit complete", state="complete", expanded=False)
        except Exception as exc:
            status.update(label="Audit failed", state="error", expanded=True)
            st.error(str(exc))

result = st.session_state.audit_result

if result:
    decision = result["decision"]
    decision_text = decision.get("decision", "HUMAN_REVIEW")
    risk = decision.get("risk_score", "—")

    if decision_text == "APPROVE":
        icon = "🟢"
    elif decision_text == "REJECT":
        icon = "🔴"
    else:
        icon = "🟡"

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="result">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="small">AUDIT RESULT</div>'
        f'<div class="decision">{icon} {decision_text.replace("_", " ")}</div>',
        unsafe_allow_html=True
    )

    a, b, c = st.columns(3)
    with a:
        st.markdown(f'<div class="metric"><div class="small">Risk score</div><b>{risk}/100</b></div>', unsafe_allow_html=True)
    with b:
        verified = result["verification"].get("verification_status", "—")
        st.markdown(f'<div class="metric"><div class="small">Verification</div><b>{verified}</b></div>', unsafe_allow_html=True)
    with c:
        issue_count = len(decision.get("issues", []))
        st.markdown(f'<div class="metric"><div class="small">Issues found</div><b>{issue_count}</b></div>', unsafe_allow_html=True)

    st.write("")
    st.subheader("Evidence")
    extracted = result["extracted"]
    invoice_data = extracted.get("invoice", {})
    po_data = extracted.get("purchase_order", {})
    numeric = result["verification"].get("deterministic_numeric_check", {})

    e1, e2, e3 = st.columns(3)
    with e1:
        st.metric("PO total", f"₹{po_data.get('total', '—')}")
    with e2:
        st.metric("Invoice total", f"₹{invoice_data.get('total', '—')}")
    with e3:
        st.metric("Variance", f"{numeric.get('variance_percent', '—')}%")

    issues = decision.get("issues", [])
    if issues:
        st.subheader("Findings")
        for issue in issues:
            severity = issue.get("severity", "medium").upper()
            st.write(f"**{severity} — {issue.get('title', 'Issue')}**")
            st.caption(issue.get("evidence", ""))

    st.subheader("Recommendation")
    st.info(decision.get("recommended_action", decision.get("summary", "Human review recommended.")))

    st.subheader("Agent trajectories")
    names = [
        "Extraction Agent",
        "Reconciliation Agent",
        "Policy Agent",
        "Verification Agent",
        "Decision Agent",
    ]
    trajectory_file = Path(result["trajectory_path"])
    events = json.loads(trajectory_file.read_text(encoding="utf-8")) if trajectory_file.exists() else []
    for name in names:
        with st.expander(name):
            agent_events = [e for e in events if e["agent"] == name]
            if not agent_events:
                st.caption("No trajectory recorded.")
            for event in agent_events:
                st.write(f"**Action:** {event.get('action')}")
                if event.get("tool"):
                    st.write(f"**Tool:** `{event['tool']}`")
                    st.json(event.get("tool_output"))
                if event.get("output"):
                    st.json(event["output"])

    st.markdown("</div>", unsafe_allow_html=True)

st.caption("ProcureGuard provides recommendations only. Final consequential decisions remain with an authorized human reviewer.")
