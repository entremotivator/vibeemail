import streamlit as st
import os
from datetime import date
from io import BytesIO
import re

# PDF Imports
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Credit Repair Letter System",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #0f1117;
}

h1, h2, h3 {
    font-family: 'DM Serif Display', serif !important;
    color: #f0ede8 !important;
}

.main-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    color: #f0ede8;
    margin-bottom: 0.2rem;
}

.subtitle {
    color: #8a8f9e;
    font-size: 1rem;
    margin-bottom: 2rem;
    font-weight: 300;
}

.section-label {
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #c9a96e;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background: #1a1d27 !important;
    border: 1px solid #2e3245 !important;
    border-radius: 8px !important;
    color: #f0ede8 !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #c9a96e !important;
    box-shadow: 0 0 0 2px rgba(201,169,110,0.2) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #c9a96e, #a8834a) !important;
    color: #0f1117 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.75rem 2.5rem !important;
    border: none !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    width: 100%;
    letter-spacing: 0.03em;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(201,169,110,0.35) !important;
}

.stDownloadButton > button {
    background: #1a1d27 !important;
    color: #c9a96e !important;
    border: 1px solid #c9a96e !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    width: 100%;
}

.stDownloadButton > button:hover {
    background: rgba(201,169,110,0.1) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: #1a1d27;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}

.stTabs [data-baseweb="tab"] {
    color: #8a8f9e !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stTabs [aria-selected="true"] {
    background: #c9a96e !important;
    color: #0f1117 !important;
    font-weight: 600 !important;
}

.info-card {
    background: #1a1d27;
    border: 1px solid #2e3245;
    border-left: 3px solid #c9a96e;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    color: #b0b5c4;
    font-size: 0.875rem;
    line-height: 1.6;
}

.validation-error {
    background: rgba(220, 80, 80, 0.1);
    border: 1px solid rgba(220, 80, 80, 0.4);
    border-radius: 8px;
    padding: 0.75rem 1rem;
    color: #ff7b7b;
    font-size: 0.875rem;
    margin-top: 0.5rem;
}

.divider {
    border: none;
    border-top: 1px solid #2e3245;
    margin: 1.5rem 0;
}

.stSidebar {
    background: #13161f !important;
}

.stSidebar [data-testid="stSidebarNav"] {
    background: #13161f;
}

label {
    color: #b0b5c4 !important;
    font-size: 0.875rem !important;
    font-weight: 400 !important;
}

.stSuccess {
    background: rgba(60, 180, 100, 0.1) !important;
    border: 1px solid rgba(60, 180, 100, 0.3) !important;
    border-radius: 8px !important;
    color: #6ee89a !important;
}

.badge {
    display: inline-block;
    background: rgba(201,169,110,0.15);
    color: #c9a96e;
    border: 1px solid rgba(201,169,110,0.3);
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# LETTER TYPE DEFINITIONS
# ─────────────────────────────────────────
LETTER_TYPES = {
    "── CREDIT BUREAU DISPUTES ──": None,
    "FCRA 611 – Credit Bureau Dispute": {
        "law": "FCRA § 611",
        "recipient": "Credit Bureau",
        "description": "Dispute inaccurate or unverifiable items on your credit report under the Fair Credit Reporting Act.",
        "tips": "Include copies of your credit report with the disputed item highlighted."
    },
    "609 Method of Verification": {
        "law": "FCRA § 609",
        "recipient": "Credit Bureau",
        "description": "Demand the bureau provide the original source documents used to verify a tradeline.",
        "tips": "Request all records, including original signed contracts."
    },
    "FCRA 623 – Furnisher Dispute": {
        "law": "FCRA § 623",
        "recipient": "Original Creditor",
        "description": "Dispute directly with the original furnisher who reported the inaccuracy.",
        "tips": "Send certified mail with return receipt."
    },
    "Factual Dispute Letter": {
        "law": "FCRA § 611",
        "recipient": "Credit Bureau",
        "description": "Dispute a specific fact (balance, date, status) that is provably incorrect.",
        "tips": "Attach bank statements or payment records as evidence."
    },
    "── DEBT COLLECTION ──": None,
    "Debt Validation Letter (FDCPA § 809)": {
        "law": "FDCPA § 809",
        "recipient": "Debt Collector",
        "description": "Force a debt collector to prove the debt is valid and they have the legal right to collect it.",
        "tips": "Must be sent within 30 days of first contact for full protections."
    },
    "Cease & Desist Communication Letter": {
        "law": "FDCPA § 805(c)",
        "recipient": "Debt Collector",
        "description": "Legally instruct a collector to stop all contact with you.",
        "tips": "Send certified mail. Collector may still sue after this."
    },
    "Pay-for-Delete Negotiation": {
        "law": "FCRA",
        "recipient": "Debt Collector / Creditor",
        "description": "Offer to pay a debt in exchange for its removal from your credit report.",
        "tips": "Get any agreement IN WRITING before making payment."
    },
    "── GOODWILL & REMOVAL REQUESTS ──": None,
    "Goodwill Deletion Request": {
        "law": "Goodwill Appeal",
        "recipient": "Original Creditor",
        "description": "Appeal to a creditor's goodwill to remove a negative item due to extenuating circumstances.",
        "tips": "Be personal and honest. Mention a good payment history before the issue."
    },
    "Late Payment Removal": {
        "law": "FCRA / Goodwill",
        "recipient": "Original Creditor",
        "description": "Request removal of a late payment mark, citing error or hardship.",
        "tips": "Works best when the late payment was an isolated incident."
    },
    "Charge-Off Dispute": {
        "law": "FCRA § 611",
        "recipient": "Credit Bureau / Creditor",
        "description": "Challenge a charge-off entry for inaccurate information or request removal after payment.",
        "tips": "Verify the charge-off date and balance are reporting accurately."
    },
    "── INQUIRIES & IDENTITY ──": None,
    "Hard Inquiry Removal": {
        "law": "FCRA § 604",
        "recipient": "Credit Bureau",
        "description": "Dispute an unauthorized hard inquiry that appeared on your report.",
        "tips": "Inquiries made without permissible purpose are illegal under FCRA."
    },
    "Identity Theft Dispute (Section 605B)": {
        "law": "FCRA § 605B",
        "recipient": "Credit Bureau",
        "description": "Block fraudulent accounts and inquiries resulting from identity theft.",
        "tips": "Include an FTC Identity Theft Report. File a police report if possible."
    },
    "Mixed File Dispute": {
        "law": "FCRA § 611",
        "recipient": "Credit Bureau",
        "description": "Dispute tradelines belonging to another person that appear on your report.",
        "tips": "Provide proof of your identity to distinguish your file from the other person's."
    },
    "── SPECIALIZED ──": None,
    "Student Loan Dispute": {
        "law": "FCRA / HEA",
        "recipient": "Credit Bureau / Servicer",
        "description": "Challenge inaccurate student loan reporting including payment status or balance.",
        "tips": "Request your payment history directly from your servicer."
    },
    "Medical Debt Dispute": {
        "law": "FCRA / FDCPA",
        "recipient": "Credit Bureau / Collector",
        "description": "Dispute medical debt collections, which have special rules under CFPB guidance.",
        "tips": "Medical debts under $500 may now be excluded from credit reports."
    },
    "Bankruptcy Notation Dispute": {
        "law": "FCRA § 611",
        "recipient": "Credit Bureau",
        "description": "Challenge inaccurate bankruptcy entries, including discharged accounts still showing balances.",
        "tips": "Obtain your bankruptcy discharge paperwork from PACER.gov."
    },
}

# Filter to only actual letter types (not section headers)
SELECTABLE_LETTERS = {k: v for k, v in LETTER_TYPES.items() if v is not None}

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
st.sidebar.markdown('<p class="section-label">AI Provider</p>', unsafe_allow_html=True)

ai_provider = st.sidebar.selectbox(
    "Provider",
    ["Anthropic (Claude)", "OpenAI (GPT)"],
    label_visibility="collapsed"
)

st.sidebar.markdown('<p class="section-label">API Key</p>', unsafe_allow_html=True)

if "Anthropic" in ai_provider:
    api_key = st.sidebar.text_input(
        "Anthropic API Key",
        type="password",
        value=os.getenv("ANTHROPIC_API_KEY", ""),
        placeholder="sk-ant-...",
        label_visibility="collapsed"
    )
    model_options = ["claude-opus-4-5", "claude-sonnet-4-5", "claude-haiku-4-5"]
else:
    api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        value=os.getenv("OPENAI_API_KEY", ""),
        placeholder="sk-...",
        label_visibility="collapsed"
    )
    model_options = ["gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano"]

st.sidebar.markdown('<p class="section-label">Model</p>', unsafe_allow_html=True)
model_name = st.sidebar.selectbox("Model", model_options, label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.markdown('<p class="section-label">Letter Tone</p>', unsafe_allow_html=True)
tone = st.sidebar.select_slider(
    "Tone",
    options=["Polite", "Firm", "Assertive", "Aggressive"],
    value="Firm",
    label_visibility="collapsed"
)

st.sidebar.markdown('<p class="section-label">Output Format</p>', unsafe_allow_html=True)
letter_format = st.sidebar.radio(
    "Format",
    ["Standard Block", "Full Block", "Modified Block"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="color: #555e72; font-size: 0.78rem; line-height: 1.6;">
<b style="color: #c9a96e;">Disclaimer</b><br>
This tool generates template letters for informational purposes only. 
It is not legal advice. Consult a licensed credit attorney for complex disputes.
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# MAIN HEADER
# ─────────────────────────────────────────
st.markdown('<h1 class="main-title">📋 Credit Repair Letter System</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Generate legally structured dispute letters · 15+ templates · Professional PDF export</p>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────
# STEP 1 – LETTER TYPE
# ─────────────────────────────────────────
st.markdown('<p class="section-label">Step 1 — Select Letter Type</p>', unsafe_allow_html=True)

letter_type = st.selectbox(
    "Letter Type",
    options=list(SELECTABLE_LETTERS.keys()),
    label_visibility="collapsed"
)

# Show letter info card
if letter_type in SELECTABLE_LETTERS and SELECTABLE_LETTERS[letter_type]:
    info = SELECTABLE_LETTERS[letter_type]
    st.markdown(f"""
    <div class="info-card">
        <span class="badge">{info['law']}</span>&nbsp;&nbsp;<span class="badge">→ {info['recipient']}</span>
        <br><br>
        <b style="color: #f0ede8;">{letter_type}</b><br>
        {info['description']}<br><br>
        <b style="color: #c9a96e;">💡 Tip:</b> {info['tips']}
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────
# STEP 2 – SENDER INFORMATION
# ─────────────────────────────────────────
st.markdown('<p class="section-label">Step 2 — Your Information</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    full_name = st.text_input("Full Name *", placeholder="Jane M. Smith")
with col2:
    address = st.text_input("Street Address *", placeholder="123 Main Street, Apt 4B")
with col3:
    city_state_zip = st.text_input("City, State ZIP *", placeholder="Atlanta, GA 30301")

col4, col5, col6 = st.columns(3)
with col4:
    ssn_last4 = st.text_input("SSN Last 4 Digits", placeholder="XXXX", max_chars=4)
with col5:
    dob = st.text_input("Date of Birth", placeholder="MM/DD/YYYY")
with col6:
    phone = st.text_input("Phone (Optional)", placeholder="(404) 555-0100")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────
# STEP 3 – RECIPIENT INFORMATION
# ─────────────────────────────────────────
st.markdown('<p class="section-label">Step 3 — Bureau / Creditor / Collector</p>', unsafe_allow_html=True)

col7, col8 = st.columns(2)
with col7:
    company_name = st.text_input("Company Name *", placeholder="Experian Information Solutions")
    company_address = st.text_area("Company Address *", placeholder="P.O. Box 4500\nAllen, TX 75013", height=90)
with col8:
    recipient_attn = st.text_input("Attn: Department (Optional)", placeholder="Consumer Disputes Department")
    company_phone = st.text_input("Company Phone (Optional)", placeholder="1-888-397-3742")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────
# STEP 4 – ACCOUNT DETAILS
# ─────────────────────────────────────────
st.markdown('<p class="section-label">Step 4 — Account / Dispute Details</p>', unsafe_allow_html=True)

col9, col10, col11 = st.columns(3)
with col9:
    account_name = st.text_input("Account / Creditor Name *", placeholder="Capital One Bank")
with col10:
    account_number = st.text_input("Account Number (Last 4 Only)", placeholder="5678", max_chars=4)
with col11:
    account_balance = st.text_input("Disputed Balance (Optional)", placeholder="$1,247.00")

col12, col13 = st.columns(2)
with col12:
    open_date = st.text_input("Account Open Date (Optional)", placeholder="January 2019")
with col13:
    reporting_date = st.text_input("Date of Negative Reporting (Optional)", placeholder="March 2023")

dispute_reason = st.text_area(
    "Describe the Issue in Detail *",
    placeholder="Example: This account does not belong to me. I have never opened an account with Capital One Bank. This appears to be a result of identity theft or a mixed credit file. The account shows a balance of $1,247.00 and was opened in January 2019, but I have no knowledge of this account.",
    height=130
)

enclosures = st.multiselect(
    "Enclosures / Documents Attached",
    [
        "Copy of Driver's License",
        "Copy of Social Security Card",
        "Utility Bill (Proof of Address)",
        "Highlighted Credit Report",
        "Police Report",
        "FTC Identity Theft Report",
        "Bank Statement",
        "Payment Receipt",
        "PACER Bankruptcy Documents",
        "Dispute Correspondence (Prior Letters)",
    ]
)

today_date = date.today().strftime("%B %d, %Y")

# ─────────────────────────────────────────
# VALIDATION
# ─────────────────────────────────────────
def validate_inputs():
    errors = []
    if not full_name.strip():
        errors.append("Full Name is required.")
    if not address.strip():
        errors.append("Street Address is required.")
    if not city_state_zip.strip():
        errors.append("City, State ZIP is required.")
    if not company_name.strip():
        errors.append("Company Name is required.")
    if not company_address.strip():
        errors.append("Company Address is required.")
    if not account_name.strip():
        errors.append("Account / Creditor Name is required.")
    if not dispute_reason.strip():
        errors.append("Dispute description is required.")
    if ssn_last4 and not ssn_last4.isdigit():
        errors.append("SSN Last 4 must be numeric only.")
    if account_number and not account_number.isdigit():
        errors.append("Account Number must be numeric only.")
    if len(dispute_reason.strip()) < 30:
        errors.append("Please provide a more detailed dispute description (at least 30 characters).")
    return errors

# ─────────────────────────────────────────
# PROMPT BUILDER
# ─────────────────────────────────────────
def build_prompt():
    info = SELECTABLE_LETTERS.get(letter_type, {})
    law_ref = info.get("law", "FCRA/FDCPA") if info else "FCRA/FDCPA"
    recipient_type = info.get("recipient", "Bureau/Creditor") if info else "Bureau/Creditor"

    enc_text = ""
    if enclosures:
        enc_text = f"\nEnclosed documents: {', '.join(enclosures)}"

    extras = []
    if account_balance:
        extras.append(f"Disputed balance: {account_balance}")
    if open_date:
        extras.append(f"Account open date: {open_date}")
    if reporting_date:
        extras.append(f"Date of negative reporting: {reporting_date}")

    return f"""You are a professional credit repair legal specialist. Write a complete, formal {letter_type}.

SENDER: {full_name}, {address}, {city_state_zip}
RECIPIENT: {company_name} ({recipient_type})
ACCOUNT: {account_name}, ending in {account_number or 'N/A'}
{chr(10).join(extras)}

DISPUTE ISSUE:
{dispute_reason}
{enc_text}

INSTRUCTIONS:
- Tone: {tone}
- Format: {letter_format}
- Cite {law_ref} specifically and accurately
- Use formal legal letter structure with clear paragraphs
- Include a specific demand / requested action
- Do NOT include the sender address block, date, recipient address, RE line, or signature — those are handled separately
- Return ONLY the body paragraphs as HTML <p> tags
- Use <strong> for key legal citations or demands
- Do not use bullet points
- Minimum 4 paragraphs, maximum 7 paragraphs
- Be professional, precise, and legally sound
"""

# ─────────────────────────────────────────
# HTML TEMPLATE
# ─────────────────────────────────────────
def build_html(body_content):
    attn_line = f"Attn: {recipient_attn}<br>" if recipient_attn.strip() else ""
    enc_html = ""
    if enclosures:
        enc_html = "<p><strong>Enclosures:</strong><br>" + "<br>".join(enclosures) + "</p>"
    phone_line = f"<br>Phone: {phone}" if phone.strip() else ""

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Credit Dispute Letter – {full_name}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Source+Sans+3:wght@300;400;600&display=swap');
body {{
    font-family: 'Source Sans 3', Arial, sans-serif;
    background: #f5f3ef;
    padding: 48px;
    color: #1a1a1a;
    font-size: 15px;
    line-height: 1.75;
}}
.letter {{
    background: white;
    max-width: 820px;
    margin: 0 auto;
    padding: 72px 80px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    border-top: 4px solid #1a3a5c;
}}
.header-bar {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 40px;
    padding-bottom: 24px;
    border-bottom: 1px solid #e8e4dc;
}}
.sender-block {{
    font-family: 'Libre Baskerville', Georgia, serif;
    font-size: 1.05rem;
}}
.sender-name {{
    font-size: 1.25rem;
    font-weight: 700;
    color: #1a3a5c;
    margin-bottom: 4px;
}}
.date-block {{
    text-align: right;
    color: #555;
    font-size: 0.9rem;
}}
.recipient-block {{
    margin-bottom: 32px;
    font-size: 0.95rem;
    color: #333;
    line-height: 1.6;
}}
.re-line {{
    font-family: 'Libre Baskerville', Georgia, serif;
    font-weight: 700;
    font-size: 1rem;
    color: #1a3a5c;
    border-left: 3px solid #1a3a5c;
    padding-left: 12px;
    margin: 28px 0;
}}
.salutation {{
    margin-bottom: 20px;
    font-size: 0.95rem;
}}
.body p {{
    margin-bottom: 18px;
    text-align: justify;
}}
.account-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 28px 0;
    font-size: 0.875rem;
}}
.account-table td {{
    padding: 8px 12px;
    border: 1px solid #e8e4dc;
}}
.account-table td:first-child {{
    background: #f7f5f1;
    font-weight: 600;
    color: #1a3a5c;
    width: 35%;
}}
.signature-block {{
    margin-top: 40px;
}}
.signature-name {{
    font-family: 'Libre Baskerville', Georgia, serif;
    font-size: 1.1rem;
    color: #1a3a5c;
    margin-top: 40px;
    border-top: 1px solid #333;
    padding-top: 8px;
    display: inline-block;
    min-width: 250px;
}}
.enclosures {{
    margin-top: 28px;
    font-size: 0.875rem;
    color: #555;
    border-top: 1px solid #e8e4dc;
    padding-top: 16px;
}}
.footer {{
    margin-top: 32px;
    font-size: 0.75rem;
    color: #aaa;
    text-align: center;
    border-top: 1px solid #e8e4dc;
    padding-top: 12px;
}}
</style>
</head>
<body>
<div class="letter">

<div class="header-bar">
  <div class="sender-block">
    <div class="sender-name">{full_name}</div>
    {address}<br>
    {city_state_zip}{phone_line}
  </div>
  <div class="date-block">{today_date}</div>
</div>

<div class="recipient-block">
  <strong>{company_name}</strong><br>
  {attn_line}
  {company_address.replace(chr(10), "<br>")}
</div>

<div class="re-line">Re: {letter_type}</div>

<div class="salutation">Dear {company_name} Consumer Disputes Department:</div>

<div class="body">
{body_content}
</div>

<table class="account-table">
  <tr><td>Account Name</td><td>{account_name}</td></tr>
  <tr><td>Account Number</td><td>XXXX-XXXX-XXXX-{account_number or "XXXX"}</td></tr>
  {"<tr><td>Disputed Balance</td><td>" + account_balance + "</td></tr>" if account_balance else ""}
  {"<tr><td>Account Open Date</td><td>" + open_date + "</td></tr>" if open_date else ""}
  {"<tr><td>Date of Negative Reporting</td><td>" + reporting_date + "</td></tr>" if reporting_date else ""}
  <tr><td>SSN (Last 4)</td><td>XXX-XX-{ssn_last4 or "XXXX"}</td></tr>
  <tr><td>Date of Birth</td><td>{dob or "On File"}</td></tr>
</table>

<div class="signature-block">
  <p>Sincerely,</p>
  <br><br>
  <span class="signature-name">{full_name}</span>
</div>

{"<div class='enclosures'>" + enc_html + "</div>" if enclosures else ""}

<div class="footer">
  Sent via Certified Mail, Return Receipt Requested · {today_date}
</div>

</div>
</body>
</html>"""

# ─────────────────────────────────────────
# PDF GENERATOR
# ─────────────────────────────────────────
def generate_pdf(body_html):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=LETTER,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
        title=f"Credit Dispute Letter – {full_name}",
        author=full_name
    )

    styles = getSampleStyleSheet()
    dark_blue = colors.HexColor("#1a3a5c")

    name_style = ParagraphStyle("NameStyle", fontSize=15, fontName="Times-Bold", textColor=dark_blue, spaceAfter=4)
    normal_style = ParagraphStyle("Normal", fontSize=11, leading=17, spaceAfter=6)
    bold_style = ParagraphStyle("Bold", fontSize=11, leading=17, fontName="Helvetica-Bold", spaceAfter=10)
    re_style = ParagraphStyle("RE", fontSize=12, fontName="Times-Bold", textColor=dark_blue, spaceAfter=14, spaceBefore=10)
    body_style = ParagraphStyle("Body", fontSize=11, leading=18, spaceAfter=12, alignment=4)  # justified
    small_style = ParagraphStyle("Small", fontSize=9, textColor=colors.grey, spaceAfter=4)

    story = []

    # Sender
    story.append(Paragraph(full_name, name_style))
    story.append(Paragraph(address, normal_style))
    story.append(Paragraph(city_state_zip, normal_style))
    if phone:
        story.append(Paragraph(phone, normal_style))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(today_date, normal_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e8e4dc"), spaceAfter=14))

    # Recipient
    story.append(Paragraph(f"<b>{company_name}</b>", normal_style))
    if recipient_attn:
        story.append(Paragraph(f"Attn: {recipient_attn}", normal_style))
    for line in company_address.split("\n"):
        if line.strip():
            story.append(Paragraph(line.strip(), normal_style))
    story.append(Spacer(1, 0.2 * inch))

    # RE line
    story.append(HRFlowable(width="4%", thickness=3, color=dark_blue, spaceAfter=6))
    story.append(Paragraph(f"Re: {letter_type}", re_style))

    # Salutation
    story.append(Paragraph(f"Dear {company_name} Consumer Disputes Department:", normal_style))
    story.append(Spacer(1, 0.1 * inch))

    # Body paragraphs
    paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", body_html, re.DOTALL | re.IGNORECASE)
    for p in paragraphs:
        clean = re.sub(r"<strong>(.*?)</strong>", r"<b>\1</b>", p.strip())
        clean = re.sub(r"<em>(.*?)</em>", r"<i>\1</i>", clean)
        clean = re.sub(r"<[^>]+>", "", clean)
        if clean:
            story.append(Paragraph(clean, body_style))

    story.append(Spacer(1, 0.2 * inch))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e8e4dc"), spaceAfter=10))

    # Account table
    account_rows = [
        ("Account Name", account_name),
        ("Account Number", f"XXXX-XXXX-XXXX-{account_number or 'XXXX'}"),
    ]
    if account_balance:
        account_rows.append(("Disputed Balance", account_balance))
    if open_date:
        account_rows.append(("Account Open Date", open_date))
    if reporting_date:
        account_rows.append(("Date of Negative Reporting", reporting_date))
    account_rows.append(("SSN (Last 4)", f"XXX-XX-{ssn_last4 or 'XXXX'}"))
    account_rows.append(("Date of Birth", dob or "On File"))

    for label, value in account_rows:
        story.append(Paragraph(f"<b>{label}:</b>  {value}", normal_style))

    story.append(Spacer(1, 0.4 * inch))

    # Signature
    story.append(Paragraph("Sincerely,", normal_style))
    story.append(Spacer(1, 0.6 * inch))
    story.append(HRFlowable(width="40%", thickness=0.5, color=colors.black, spaceAfter=4))
    story.append(Paragraph(f"<b>{full_name}</b>", bold_style))

    # Enclosures
    if enclosures:
        story.append(Spacer(1, 0.3 * inch))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e8e4dc"), spaceAfter=8))
        story.append(Paragraph("<b>Enclosures:</b>", normal_style))
        for enc in enclosures:
            story.append(Paragraph(f"• {enc}", small_style))

    # Footer
    story.append(Spacer(1, 0.4 * inch))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e8e4dc"), spaceAfter=6))
    story.append(Paragraph(f"Sent via Certified Mail, Return Receipt Requested · {today_date}", small_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ─────────────────────────────────────────
# GENERATE BUTTON
# ─────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    generate_clicked = st.button("⚡ Generate Letter", use_container_width=True)

if generate_clicked:
    errors = validate_inputs()
    if errors:
        for error in errors:
            st.markdown(f'<div class="validation-error">⚠️ {error}</div>', unsafe_allow_html=True)
    else:
        with st.spinner("Drafting your letter..."):
            try:
                if "Anthropic" in ai_provider:
                    import anthropic
                    client = anthropic.Anthropic(api_key=api_key if api_key else None)
                    message = client.messages.create(
                        model=model_name,
                        max_tokens=2048,
                        system="You are a professional credit repair legal specialist with 20 years of experience. You write precise, legally sound dispute letters.",
                        messages=[{"role": "user", "content": build_prompt()}]
                    )
                    body_content = message.content[0].text
                else:
                    from openai import OpenAI
                    client = OpenAI(api_key=api_key if api_key else None)
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": "You are a professional credit repair legal specialist with 20 years of experience."},
                            {"role": "user", "content": build_prompt()}
                        ]
                    )
                    body_content = response.choices[0].message.content

                final_html = build_html(body_content)

                st.success("✅ Letter generated successfully!")

                tab1, tab2, tab3 = st.tabs(["📄 Preview", "💾 Download", "🔤 Raw HTML"])

                with tab1:
                    st.components.v1.html(final_html, height=900, scrolling=True)

                with tab2:
                    st.markdown('<p class="section-label">Download Your Letter</p>', unsafe_allow_html=True)

                    dl_col1, dl_col2 = st.columns(2)

                    with dl_col1:
                        safe_name = re.sub(r"[^a-zA-Z0-9]", "_", full_name.lower())
                        st.download_button(
                            "📄 Download PDF",
                            generate_pdf(body_content),
                            file_name=f"credit_dispute_{safe_name}_{date.today().isoformat()}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )

                    with dl_col2:
                        st.download_button(
                            "🌐 Download HTML",
                            final_html,
                            file_name=f"credit_dispute_{safe_name}_{date.today().isoformat()}.html",
                            mime="text/html",
                            use_container_width=True
                        )

                    st.markdown("""
                    <div class="info-card">
                        <b style="color: #f0ede8;">Next Steps</b><br>
                        1. Print the letter and sign in <b>blue ink</b><br>
                        2. Make 2 copies of everything before mailing<br>
                        3. Send via <b>Certified Mail with Return Receipt</b> (USPS Form 3811)<br>
                        4. Keep your tracking number and receipt<br>
                        5. Bureaus have <b>30 days</b> to respond (45 days if you provide additional info)<br>
                        6. Follow up if you receive no response within 35 days
                    </div>
                    """, unsafe_allow_html=True)

                with tab3:
                    st.code(final_html, language="html")

            except ImportError as e:
                if "anthropic" in str(e).lower():
                    st.error("Anthropic library not installed. Run: pip install anthropic")
                else:
                    st.error(f"Missing library: {e}")
            except Exception as e:
                st.error(f"Error generating letter: {e}")
                st.info("Make sure your API key is correct and you have sufficient credits.")
            
