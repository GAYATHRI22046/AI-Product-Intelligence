import streamlit as st
from dotenv import load_dotenv
from google import genai
import os
import json
import html
import textwrap
import fitz
import requests
from bs4 import BeautifulSoup

# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Product Intelligence",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM THEME
# ============================================================

st.markdown(textwrap.dedent(
        """
    <style>
    html, body, [class*="css"] {
        font-family: "Segoe UI", sans-serif;
    }

    .stApp {
        background: #f4f7fb;
    }

    .block-container {
        padding-top: 1.35rem;
        padding-bottom: 2.5rem;
        max-width: 1480px;
    }

    h1, h2, h3, h4 {
        color: #111827 !important;
    }

    p, label, span {
        color: #374151;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background: #07182d;
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    section[data-testid="stSidebar"] .stTextArea textarea,
    section[data-testid="stSidebar"] input {
        background: #102641 !important;
        color: white !important;
        border: 1px solid #29496d !important;
    }

    section[data-testid="stSidebar"] button {
        background: #ef4444 !important;
        color: white !important;
        border: none !important;
        font-weight: 700 !important;
    }

    section[data-testid="stSidebar"] .stCheckbox label {
        color: #f8fafc !important;
    }

    /* HERO */
    .hero {
        background: linear-gradient(135deg, #0b1f3a, #102f55);
        border-radius: 18px;
        padding: 27px 30px;
        margin-bottom: 20px;
        border: 1px solid #183b67;
        color: white;
    }

    .hero-layout {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 25px;
    }

    .hero-left {
        flex: 1.3;
    }

    .hero-title {
        color: white !important;
        font-size: 30px;
        font-weight: 800;
        margin-bottom: 7px;
    }

    .hero-subtitle {
        color: #cbd5e1 !important;
        font-size: 15px;
        line-height: 1.5;
        max-width: 620px;
    }

    .hero-badge {
        display: inline-block;
        margin-top: 14px;
        padding: 6px 12px;
        border-radius: 18px;
        background: #243f72;
        color: #dbeafe !important;
        font-size: 12px;
        font-weight: 700;
    }

    .hero-flow {
        display: flex;
        align-items: center;
        gap: 17px;
        min-width: 475px;
        justify-content: flex-end;
    }

    .hero-step {
        text-align: center;
        min-width: 92px;
    }

    .hero-icon {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        margin: 0 auto 6px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #153b6a;
        font-size: 23px;
    }

    .hero-step-title {
        color: white !important;
        font-size: 14px;
        font-weight: 800;
    }

    .hero-step-sub {
        color: #b8c7dc !important;
        font-size: 10px;
        line-height: 1.25;
        margin-top: 3px;
    }

    .hero-arrow {
        color: #dbeafe !important;
        font-size: 22px;
    }

    /* SECTION */
    .section-heading {
        font-size: 18px;
        font-weight: 800;
        color: #102a50 !important;
        margin-top: 16px;
        margin-bottom: 10px;
    }

    .section-caption {
        color: #64748b !important;
        font-size: 12px;
        margin-top: -5px;
        margin-bottom: 10px;
    }

    /* PRODUCT */
    .product-card {
        background: white;
        border: 1px solid #dbe5f1;
        border-radius: 13px;
        padding: 15px 20px;
        min-height: 78px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.035);
    }

    .product-label {
        color: #5273a0 !important;
        font-size: 10px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: .8px;
    }

    .product-name {
        color: #102a50 !important;
        font-size: 17px;
        font-weight: 800;
        margin-top: 6px;
    }

    /* KPI */
    .kpi-card {
        background: white;
        border: 1px solid #dbe5f1;
        border-radius: 12px;
        padding: 14px 16px;
        min-height: 92px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.035);
    }

    .kpi-card.primary {
        background: linear-gradient(135deg, #1762b7, #1f4f91);
        border: none;
    }

    .kpi-icon {
        font-size: 20px;
    }

    .kpi-label {
        color: #547095 !important;
        font-size: 11px;
        margin-top: 4px;
    }

    .kpi-card.primary .kpi-label {
        color: #dbeafe !important;
    }

    .kpi-value {
        color: #102a50 !important;
        font-size: 25px;
        font-weight: 800;
        margin-top: 2px;
    }

    .kpi-card.primary .kpi-value {
        color: white !important;
    }

    /* SCORE BREAKDOWN */
    .breakdown-card {
        background: white;
        border: 1px solid #dbe5f1;
        border-radius: 12px;
        padding: 13px 15px;
        min-height: 104px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.035);
    }

    .breakdown-title {
        color: #36577f !important;
        font-size: 11px;
        font-weight: 700;
    }

    .breakdown-value {
        color: #102a50 !important;
        font-size: 22px;
        font-weight: 800;
        margin-top: 5px;
    }

    .bar-bg {
        background: #e8eef7;
        border-radius: 8px;
        height: 7px;
        margin-top: 9px;
        overflow: hidden;
    }

    .bar-fill {
        height: 7px;
        border-radius: 8px;
        background: #398ef3;
    }

    /* RISKS */
    .risk-card {
        background: white;
        border: 1px solid #dbe5f1;
        border-radius: 13px;
        padding: 13px 15px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.035);
        height: 100%;
    }

    .risk-title {
        color: #18375e !important;
        font-size: 14px;
        font-weight: 800;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .risk-count {
        background: #ec4899;
        color: white !important;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        font-size: 11px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
    }

    .missing-item {
        color: #5b2142 !important;
        padding: 3px 0;
        margin-bottom: 4px;
        font-size: 12px;
        line-height: 1.4;
        font-weight: 600;
    }

    .missing-number {
        color: #be185d !important;
        font-weight: 800;
        margin-right: 5px;
    }

    .conflict-item {
        background: #fff1f2;
        border: 1px solid #fecdd3;
        border-left: 4px solid #ef4444;
        color: #7f1d1d !important;
        border-radius: 8px;
        padding: 9px 10px;
        margin-bottom: 7px;
        font-size: 12px;
        line-height: 1.4;
        font-weight: 600;
    }

    /* QUESTIONS */
    .question-item {
        background: white;
        border: 1px solid #dbe5f1;
        border-radius: 9px;
        padding: 9px 12px;
        margin-bottom: 6px;
        color: #18375e !important;
        font-size: 12px;
        font-weight: 600;
    }

    /* SPEC TABLE */
    .spec-table {
        background: white;
        border: 1px solid #dbe5f1;
        border-radius: 13px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.035);
    }

    .spec-row {
        display: grid;
        grid-template-columns: 1.25fr .9fr .75fr 1.05fr;
        padding: 10px 15px;
        border-bottom: 1px solid #edf2f7;
        align-items: center;
        min-height: 39px;
    }

    .spec-row:last-child {
        border-bottom: none;
    }

    .spec-header {
        background: #f7f9fc;
        color: #607896 !important;
        font-size: 9px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: .6px;
    }

    .spec-name {
        color: #18375e !important;
        font-size: 11px;
        font-weight: 700;
    }

    .spec-value {
        color: #36577f !important;
        font-size: 11px;
        font-weight: 600;
    }

    .verified {
        color: #15803d !important;
        font-size: 11px;
        font-weight: 700;
    }

    .not-found {
        color: #dc2626 !important;
        font-size: 11px;
        font-weight: 700;
    }

    /* DETAIL */
    .detail-card {
        background: white;
        border: 1px solid #dbe5f1;
        border-radius: 13px;
        padding: 15px 17px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.035);
    }

    .detail-title {
        color: #17385f !important;
        font-size: 16px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .detail-value {
        color: #102a50 !important;
        font-size: 21px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .detail-label {
        color: #5273a0 !important;
        font-size: 11px;
        font-weight: 600;
    }

    .meaning-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 9px;
        padding: 10px 12px;
        margin-top: 13px;
        color: #374151 !important;
        font-size: 12px;
        line-height: 1.5;
    }

    .evidence-box {
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-left: 4px solid #2563eb;
        border-radius: 8px;
        padding: 9px 11px;
        color: #1f2937 !important;
        font-family: Consolas, "Courier New", monospace;
        font-size: 11px;
        line-height: 1.45;
        word-break: break-word;
        margin-top: 8px;
    }

    .evidence-meta {
        display: flex;
        gap: 7px;
        flex-wrap: wrap;
        margin-top: 8px;
    }

    .meta-pill {
        display: inline-block;
        background: #f1f5f9;
        color: #334155 !important;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 4px 7px;
        font-size: 10px;
        font-weight: 600;
    }

    /* FOOTER */
    .footer {
        text-align: center;
        color: #94a3b8 !important;
        margin-top: 35px;
        padding-top: 17px;
        border-top: 1px solid #dbe5f1;
        font-size: 12px;
    }

    /* STREAMLIT SPACING */
    div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stExpander"]) {
        margin-bottom: 4px;
    }

    [data-testid="stMetricValue"] {
        color: #102a50 !important;
    }
    </style>
    """
    ), unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## 📥 Product Input")
    st.caption("Analyze industrial product information from multiple sources.")

    product_text = st.text_area(
        "Manual Information",
        height=150,
        placeholder="Paste motor specifications, catalog text or technical information..."
    )

    uploaded_pdf = st.file_uploader(
        "Upload Product PDF",
        type=["pdf"]
    )

    website_url = st.text_input(
        "Product Website URL",
        placeholder="https://example.com/product"
    )

    st.divider()

    analyze_button = st.button(
        "🚀 Analyze Product",
        type="primary",
        use_container_width=True
    )

# ============================================================
# API CLIENT
# ============================================================

client = None

if api_key:
    client = genai.Client(api_key=api_key)

# ============================================================
# PDF EXTRACTION
# ============================================================

pdf_text = ""

if uploaded_pdf:
    try:
        pdf_document = fitz.open(
            stream=uploaded_pdf.read(),
            filetype="pdf"
        )

        for page_number, page in enumerate(pdf_document, start=1):
            page_text = page.get_text()
            pdf_text += (
                f"\n\n--- PDF PAGE {page_number} ---\n"
                f"{page_text}"
            )

        if pdf_text.strip():
            st.sidebar.success(
                f"✓ PDF loaded • {len(pdf_document)} pages"
            )
        else:
            st.sidebar.warning("PDF contains no readable text.")

    except Exception as e:
        st.sidebar.error(f"PDF error: {e}")

# ============================================================
# WEBSITE EXTRACTION
# ============================================================

website_text = ""

if website_url:
    try:
        response = requests.get(
            website_url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()

        website_text = soup.get_text(
            separator=" ",
            strip=True
        )

        if website_text:
            st.sidebar.success("✓ Website loaded")

    except Exception as e:
        st.sidebar.error(f"Website error: {e}")

# ============================================================
# HERO
# ============================================================

st.markdown(textwrap.dedent(
        """
    <div class="hero">
        <div class="hero-layout">
            <div class="hero-left">
                <div class="hero-title">⚙️ AI Product Intelligence</div>
                <div class="hero-subtitle">
                    Transform scattered industrial product information into
                    structured, explainable and traceable intelligence.
                </div>
                <div class="hero-badge">
                    ⚙️ AI-Powered Industrial Commerce Intelligence
                </div>
            </div>
            <div class="hero-flow">
                <div class="hero-step">
                    <div class="hero-icon">📄</div>
                    <div class="hero-step-title">Extract</div>
                    <div class="hero-step-sub">From PDFs, websites<br>and documents</div>
                </div>
                <div class="hero-arrow">→</div>
                <div class="hero-step">
                    <div class="hero-icon">🧠</div>
                    <div class="hero-step-title">Understand</div>
                    <div class="hero-step-sub">Convert to clear<br>intelligence</div>
                </div>
                <div class="hero-arrow">→</div>
                <div class="hero-step">
                    <div class="hero-icon">🔎</div>
                    <div class="hero-step-title">Verify</div>
                    <div class="hero-step-sub">Find gaps, conflicts<br>and trace sources</div>
                </div>
            </div>
        </div>
    </div>
    """
    ), unsafe_allow_html=True)

# ============================================================
# ANALYSIS
# ============================================================
#
# NOTE: st.button() only returns True on the single script run right
# after it is clicked. Any later rerun caused by another widget (for
# example the specification selectbox below) sees analyze_button as
# False again. So the freshly computed result is saved into
# st.session_state right after it is produced, and everything below
# reads from st.session_state instead of relying on analyze_button
# still being True. This keeps the analysis on screen across reruns
# without changing any of the extraction/analysis logic itself.

if analyze_button:

    if not client:
        st.error(
            "Gemini API key not found. Add GEMINI_API_KEY to your .env file."
        )
        st.stop()

    sources = []

    if pdf_text.strip():
        sources.append(
            "===== SOURCE 1: PRODUCT PDF =====\n" + pdf_text
        )

    if website_text.strip():
        sources.append(
            "===== SOURCE 2: PRODUCT WEBSITE =====\n" + website_text
        )

    if product_text.strip():
        sources.append(
            "===== SOURCE 3: MANUAL / PASTED INFORMATION =====\n" + product_text
        )

    if not sources:
        st.warning("Please provide at least one product information source.")
        st.stop()

    analysis_text = "\n\n".join(sources)

    source_names = []

    if pdf_text.strip():
        source_names.append("PDF")

    if website_text.strip():
        source_names.append("Website")

    if product_text.strip():
        source_names.append("Manual Text")

    source_type = " + ".join(source_names)

    st.info(f"Analyzing multiple sources: {source_type}")

    prompt = f"""
You are an industrial product intelligence expert.

Analyze ALL of the supplied product information sources.

IMPORTANT:
The sources may contain overlapping information.
Compare them carefully.

SOURCE INFORMATION:

{analysis_text}

YOUR TASK:

Create structured product intelligence for the electric motor.

RULES:

1. Extract every useful product specification.
2. Never invent, guess, estimate or assume values.
3. Preserve exact values from the sources.
4. Use information from ALL available sources.
5. Compare the same specification across different sources.
6. If two sources give different values for the SAME specification, identify this as a conflict.
7. Do NOT call values a conflict if they refer to different specifications.
8. Identify important information that is missing.
9. Generate practical questions that a buyer can ask the supplier about missing or conflicting information.
10. Explain every extracted specification in simple, buyer-friendly language.
11. Product Intelligence Score represents the quality, completeness and consistency of the INFORMATION. It does NOT represent whether the physical product itself is good or bad.
12. Provide evidence for every extracted specification.
13. Evidence must come ONLY from the supplied sources.
14. Never invent evidence.
15. For PDF evidence, use the PDF PAGE number.
16. For website evidence, identify it as Website.
17. For manual text evidence, identify it as Manual Text.
18. If multiple sources support the same specification, include the most useful evidence.
19. If sources disagree, make the conflict explicit.
20. Ignore navigation menus, advertisements, page numbers, repeated headers and unrelated website content.

EVIDENCE FORMAT:

For every specification provide:
source
location
snippet

If evidence cannot be identified, use:
source = "Not identified"
location = "Not identified"
snippet = "Evidence not found"

Return ONLY valid JSON matching the required schema.
"""

    try:
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": {
                    "type": "object",
                    "properties": {
                        "product_name": {"type": "string"},
                        "product_type": {"type": "string"},
                        "specifications": {
                            "type": "object",
                            "additionalProperties": {"type": "string"}
                        },
                        "technical_explanations": {
                            "type": "object",
                            "additionalProperties": {"type": "string"}
                        },
                        "missing_information": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "supplier_questions": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "conflicts": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "evidence": {
                            "type": "object",
                            "additionalProperties": {
                                "type": "object",
                                "properties": {
                                    "source": {"type": "string"},
                                    "location": {"type": "string"},
                                    "snippet": {"type": "string"}
                                },
                                "required": [
                                    "source",
                                    "location",
                                    "snippet"
                                ]
                            }
                        }
                    },
                    "required": [
                        "product_name",
                        "product_type",
                        "specifications",
                        "technical_explanations",
                        "missing_information",
                        "supplier_questions",
                        "conflicts",
                        "evidence"
                    ]
                }
            }
        )

        response_text = interaction.output_text.strip()

        if response_text.startswith("```json"):
            response_text = response_text[7:]
        elif response_text.startswith("```"):
            response_text = response_text[3:]

        if response_text.endswith("```"):
            response_text = response_text[:-3]

        result = json.loads(response_text.strip())

    except json.JSONDecodeError:
        st.error("Gemini returned an unexpected response format.")
        st.code(interaction.output_text)
        st.stop()

    except Exception as e:
        st.error(f"Analysis error: {e}")
        st.stop()

    # Persist this run's result so it survives reruns triggered by
    # other widgets (e.g. changing the specification selectbox).
    st.session_state["result"] = result
    st.session_state["source_type"] = source_type

# ============================================================
# LANDING PAGE
# (shown only when no analysis has been run yet in this session)
# ============================================================

if "result" not in st.session_state:
    st.markdown(
        '<div class="section-heading">How the platform works</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("### 📄 Extract")
            st.write(
                "Extract technical specifications from PDFs, websites "
                "and unstructured documents."
            )

    with col2:
        with st.container(border=True):
            st.markdown("### 🧠 Understand")
            st.write(
                "Convert complex engineering information into clear "
                "buyer-friendly intelligence."
            )

    with col3:
        with st.container(border=True):
            st.markdown("### 🔎 Verify")
            st.write(
                "Detect information gaps, conflicting values and trace "
                "specifications back to evidence."
            )

    st.markdown(
        '<div class="footer">⚙️ AI Product Intelligence • Industrial Commerce Intelligence Platform</div>',
        unsafe_allow_html=True
    )

    st.stop()

result = st.session_state["result"]
source_type = st.session_state["source_type"]

# ============================================================
# RESULT DATA
# ============================================================

specs = result.get("specifications", {})
missing = result.get("missing_information", [])
conflicts = result.get("conflicts", [])
evidence = result.get("evidence", {})
explanations = result.get("technical_explanations", {})
supplier_questions = result.get("supplier_questions", [])

spec_count = len(specs)
missing_count = len(missing)
conflict_count = len(conflicts)

# ============================================================
# EVIDENCE COVERAGE
# ============================================================

evidence_count = sum(
    1
    for item in evidence.values()
    if item.get("snippet") and item.get("snippet") != "Evidence not found"
)

evidence_coverage = (
    round((evidence_count / spec_count) * 100)
    if spec_count
    else 0
)

# ============================================================
# SCORE
# ============================================================

completeness_score = min(
    100,
    (spec_count / 15) * 100
)

completeness_score -= min(
    missing_count * 5,
    30
)

completeness_score = max(0, completeness_score)

consistency_score = max(
    0,
    100 - min(conflict_count * 20, 100)
)

technical_score = min(
    100,
    (spec_count / 10) * 100
)

score = round(
    completeness_score * 0.40
    + consistency_score * 0.30
    + technical_score * 0.30
)

# ============================================================
# PRODUCT OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-heading">📦 Product Overview</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns([1.25, 1])

with col1:
    st.markdown(textwrap.dedent(
        f"""
        <div class="product-card">
            <div class="product-label">PRODUCT</div>
            <div class="product-name">
                {html.escape(str(result.get("product_name", "Not identified")))}
            </div>
        </div>
        """
    ), unsafe_allow_html=True)

with col2:
    st.markdown(textwrap.dedent(
        f"""
        <div class="product-card">
            <div class="product-label">PRODUCT TYPE</div>
            <div class="product-name">
                {html.escape(str(result.get("product_type", "Not identified")))}
            </div>
        </div>
        """
    ), unsafe_allow_html=True)

st.caption(f"🔗 Sources analyzed: {source_type}")

# ============================================================
# MAIN TWO-COLUMN DASHBOARD
# (Left: Intelligence Overview -> Score Breakdown -> Spec Table)
# (Right: Information Risks -> Supplier Questions -> Detail)
# ============================================================

left_col, right_col = st.columns([1.18, 1])

# ------------------------------------------------------------
# LEFT COLUMN
# ------------------------------------------------------------

with left_col:

    # ---- Intelligence Overview ----
    st.markdown(
        '<div class="section-heading">📊 Intelligence Overview</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns([1.3, 1, 1, 1])

    kpis = [
        ("🎯", "Intelligence Score", f"{score}/100", True),
        ("⚙️", "Specifications", str(spec_count), False),
        ("⚠️", "Information Gaps", str(missing_count), False),
        ("🔀", "Conflicts", str(conflict_count), False),
    ]

    for column, (icon, label, value, primary) in zip(
        [c1, c2, c3, c4],
        kpis
    ):
        with column:
            card_class = "kpi-card primary" if primary else "kpi-card"

            st.markdown(textwrap.dedent(
        f"""
                <div class="{card_class}">
                    <div class="kpi-icon">{icon}</div>
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value">{value}</div>
                </div>
                """
    ), unsafe_allow_html=True)

    # ---- Score Breakdown ----
    st.markdown(
        '<div class="section-heading">📊 Score Breakdown</div>',
        unsafe_allow_html=True
    )

    b1, b2, b3 = st.columns(3)

    breakdown = [
        ("📋", "Completeness", completeness_score),
        ("🔗", "Consistency", consistency_score),
        ("⚙️", "Technical Coverage", technical_score)
    ]

    for column, (icon, label, value) in zip(
        [b1, b2, b3],
        breakdown
    ):
        with column:
            st.markdown(textwrap.dedent(
        f"""
                <div class="breakdown-card">
                    <div class="breakdown-title">{icon} {label}</div>
                    <div class="breakdown-value">{round(value)}/100</div>
                    <div class="bar-bg">
                        <div class="bar-fill" style="width:{min(100, max(0, value))}%"></div>
                    </div>
                </div>
                """
    ), unsafe_allow_html=True)

    # ---- Specification Intelligence ----
    st.markdown(
        '<div class="section-heading">⚙️ Specification Intelligence</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-caption">Every extracted value can be expanded to see its explanation and evidence.</div>',
        unsafe_allow_html=True
    )

    st.markdown(textwrap.dedent(
        """
        <div class="spec-table">
            <div class="spec-row spec-header">
                <div>SPECIFICATION</div>
                <div>VALUE</div>
                <div>STATUS</div>
                <div>SOURCE</div>
            </div>
        """
    ), unsafe_allow_html=True)

    for name, value in specs.items():
        item_evidence = evidence.get(name, {})

        snippet = item_evidence.get("snippet", "")
        source = item_evidence.get("source", "Unknown")
        location = item_evidence.get("location", "")

        if snippet and snippet != "Evidence not found":
            status = "✓ Verified"
            status_class = "verified"
        else:
            status = "⚠ Unverified"
            status_class = "not-found"

        source_display = source

        if location:
            source_display += f" • {location}"

        st.markdown(textwrap.dedent(
            f"""
            <div class="spec-row">
                <div class="spec-name">
                    {html.escape(name.replace("_", " ").title())}
                </div>
                <div class="spec-value">
                    {html.escape(str(value))}
                </div>
                <div class="{status_class}">
                    {status}
                </div>
                <div class="spec-value">
                    {html.escape(str(source_display))}
                </div>
            </div>
            """
        ), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# RIGHT COLUMN
# ------------------------------------------------------------

with right_col:

    # ---- Information Risks ----
    st.markdown(
        '<div class="section-heading">⚠️ Information Risks</div>',
        unsafe_allow_html=True
    )

    risk1, risk2 = st.columns(2)

    with risk1:
        st.markdown(
            f'<div class="risk-card"><div class="risk-title">🚨 Missing Information'
            f'<span class="risk-count">{missing_count}</span></div>',
            unsafe_allow_html=True
        )

        if missing:
            for index, item in enumerate(missing, start=1):
                st.markdown(textwrap.dedent(
        f"""
                    <div class="missing-item">
                        <span class="missing-number">{index}.</span>
                        {html.escape(str(item))}
                    </div>
                    """
    ), unsafe_allow_html=True)
        else:
            st.success("No major information gaps detected.")

        st.markdown("</div>", unsafe_allow_html=True)

    with risk2:
        st.markdown(
            f'<div class="risk-card"><div class="risk-title">🔀 Conflicting Information'
            f'<span class="risk-count">{conflict_count}</span></div>',
            unsafe_allow_html=True
        )

        if conflicts:
            for conflict in conflicts:
                st.markdown(textwrap.dedent(
        f"""
                    <div class="conflict-item">
                        {html.escape(str(conflict))}
                    </div>
                    """
    ), unsafe_allow_html=True)
        else:
            st.success("No conflicting specifications detected.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ---- Supplier Questions ----
    st.markdown(
        '<div class="section-heading">❓ Supplier Questions</div>',
        unsafe_allow_html=True
    )

    if supplier_questions:
        for index, question in enumerate(supplier_questions, start=1):
            st.markdown(textwrap.dedent(
                f"""
                <div class="question-item">
                    {index}. {html.escape(str(question))}
                </div>
                """
            ), unsafe_allow_html=True)
    else:
        st.success("No supplier questions generated.")

    # ---- Technical Specification Detail ----
    st.markdown(
        '<div class="section-heading">🔎 Specification Details</div>',
        unsafe_allow_html=True
    )

    if specs:
        selected_name = st.selectbox(
            "Select a specification to inspect",
            list(specs.keys()),
            format_func=lambda x: x.replace("_", " ").title(),
            label_visibility="collapsed",
            key="selected_spec"
        )
    else:
        selected_name = None

    if selected_name:
        selected_value = specs.get(selected_name, "")
        selected_explanation = explanations.get(
            selected_name,
            "No explanation available."
        )

        selected_evidence = evidence.get(
            selected_name,
            {}
        )

        selected_source = selected_evidence.get(
            "source",
            "Not identified"
        )

        selected_location = selected_evidence.get(
            "location",
            "Not identified"
        )

        selected_snippet = selected_evidence.get(
            "snippet",
            "Evidence not found"
        )

        st.markdown(textwrap.dedent(
        f"""
            <div class="detail-card">
                <div class="detail-title">
                    📄 {html.escape(selected_name.replace("_", " ").title())}
                </div>
                <div class="detail-value">
                    {html.escape(str(selected_value))}
                </div>
                <div class="detail-label">
                    Source: {html.escape(str(selected_source))}
                </div>
                <div class="detail-label">
                    Location: {html.escape(str(selected_location))}
                </div>
                <div class="meaning-box">
                    <strong>💡 What does this mean?</strong><br>
                    {html.escape(str(selected_explanation))}
                </div>
                <div style="margin-top:13px; color:#18375e; font-size:14px; font-weight:800;">
                    📌 Evidence
                </div>
                <div class="evidence-box">
                    {html.escape(str(selected_snippet))}
                </div>
            </div>
            """
    ), unsafe_allow_html=True)

# ============================================================
# TRACEABILITY
# ============================================================

st.markdown(
    '<div class="section-heading">🔎 Evidence Traceability</div>',
    unsafe_allow_html=True
)

trace1, trace2 = st.columns([1, 2])

with trace1:
    with st.container(border=True):
        st.metric(
            "Traceable Specifications",
            f"{evidence_count}/{spec_count}"
        )

with trace2:
    with st.container(border=True):
        st.write(f"**Evidence coverage: {evidence_coverage}%**")
        st.progress(evidence_coverage / 100)
        st.caption(
            "Traceability shows how many extracted specifications can be "
            "be linked back to source evidence."
        )

# ============================================================
# FOOTER
# ============================================================

st.markdown(textwrap.dedent(
        """
    <div class="footer">
        ⚙️ AI Product Intelligence • Industrial Commerce Intelligence Platform
    </div>
    """
    ), unsafe_allow_html=True)
