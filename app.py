import streamlit as st
from openai import OpenAI
import os
from datetime import date
from io import BytesIO

# PDF Imports (Required Library Usage)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Credit Repair Letter System",
    page_icon="💳",
    layout="wide"
)

st.title("💳 AI Credit Repair Letter System")
st.markdown("Generate legally structured credit repair letters with professional HTML + PDF export.")

# -----------------------------
# SIDEBAR SETTINGS
# -----------------------------
st.sidebar.title("⚙️ AI Settings")

api_key = st.sidebar.text_input(
    "OpenAI API Key (Optional)",
    type="password",
    value=os.getenv("OPENAI_API_KEY", "")
)

model_name = st.sidebar.selectbox(
    "Model",
    ["gpt-4.1-mini", "gpt-4.1-nano"],
    index=0
)

# -----------------------------
# LETTER TYPE
# -----------------------------
letter_type = st.selectbox(
    "Select Letter Type",
    [
        "Credit Bureau Dispute (FCRA 611)",
        "609 Method of Verification",
        "Debt Validation Letter (FDCPA)",
        "Goodwill Deletion Request",
        "Late Payment Removal",
        "Hard Inquiry Removal",
        "Charge-Off Dispute",
        "Identity Theft Dispute"
    ]
)

st.markdown("---")

# -----------------------------
# USER INPUT
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    full_name = st.text_input("Full Name")
    address = st.text_input("Street Address")
    city_state_zip = st.text_input("City, State ZIP")
    ssn_last4 = st.text_input("SSN (Last 4)")
    dob = st.text_input("Date of Birth")

with col2:
    company_name = st.text_input("Bureau / Creditor Name")
    company_address = st.text_area("Bureau / Creditor Address")
    account_name = st.text_input("Account / Creditor Name")
    account_number = st.text_input("Account Number (Last 4 Only)")
    dispute_reason = st.text_area("Describe the Issue in Detail")

today_date = date.today().strftime("%B %d, %Y")

# -----------------------------
# AI PROMPT BUILDER
# -----------------------------
def build_prompt():
    return f"""
Write a formal {letter_type}.

Issue:
{dispute_reason}

Account Name: {account_name}
Account Last 4: {account_number}

Use professional legal structure.
Reference FCRA or FDCPA where appropriate.
Be firm but not aggressive.
Return only HTML paragraph tags.
"""

# -----------------------------
# HTML TEMPLATE
# -----------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Credit Letter</title>
<style>
body {{
    font-family: Arial, sans-serif;
    background-color: #f2f4f8;
    padding: 40px;
}}
.container {{
    background: white;
    padding: 50px;
    max-width: 850px;
    margin: auto;
    box-shadow: 0 6px 18px rgba(0,0,0,0.1);
}}
.section {{
    margin-bottom: 18px;
    font-size: 16px;
    line-height: 1.7;
}}
.header {{
    margin-bottom: 30px;
}}
.re-line {{
    font-weight: bold;
    font-size: 18px;
}}
</style>
</head>
<body>
<div class="container">

<div class="header">
<p>{full_name}<br>
{address}<br>
{city_state_zip}</p>

<p>{today_date}</p>

<p>{company_name}<br>
{company_address}</p>
</div>

<div class="section re-line">
Re: {letter_type}
</div>

<div class="section">
{body_content}
</div>

<div class="section">
Account Name: {account_name}<br>
Account Number: XXXX-{account_number}<br>
SSN (Last 4): {ssn_last4}<br>
DOB: {dob}
</div>

<div class="section">
Sincerely,<br><br>
{full_name}
</div>

</div>
</body>
</html>
"""

# -----------------------------
# PDF GENERATOR (IN MEMORY)
# -----------------------------
def generate_pdf_buffer(text_content):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=LETTER)
    styles = getSampleStyleSheet()
    story = []

    custom_style = ParagraphStyle(
        name="Custom",
        parent=styles["Normal"],
        fontSize=12,
        leading=18,
        spaceAfter=12
    )

    for line in text_content.split("\n"):
        story.append(Paragraph(line, custom_style))
        story.append(Spacer(1, 0.15 * inch))

    doc.build(story)
    buffer.seek(0)
    return buffer

# -----------------------------
# GENERATE BUTTON
# -----------------------------
if st.button("🚀 Generate Letter"):

    try:
        with st.spinner("Generating legally structured letter..."):

            if api_key:
                client = OpenAI(api_key=api_key)
            else:
                client = OpenAI()

            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a professional credit repair legal specialist."},
                    {"role": "user", "content": build_prompt()}
                ]
            )

            body_content = response.choices[0].message.content

            # Final HTML
            final_html = HTML_TEMPLATE.format(
                full_name=full_name,
                address=address,
                city_state_zip=city_state_zip,
                today_date=today_date,
                company_name=company_name,
                company_address=company_address,
                letter_type=letter_type,
                body_content=body_content,
                account_name=account_name,
                account_number=account_number,
                ssn_last4=ssn_last4,
                dob=dob
            )

            st.success("✅ Letter Generated Successfully!")

            tab1, tab2 = st.tabs(["Preview", "HTML Code"])

            with tab1:
                st.components.v1.html(final_html, height=800, scrolling=True)

            with tab2:
                st.code(final_html, language="html")
                st.download_button(
                    "Download HTML",
                    final_html,
                    file_name="credit_letter.html",
                    mime="text/html"
                )

            # -----------------------------
            # CLEAN TEXT FOR PDF
            # -----------------------------
            clean_text = f"""
{full_name}
{address}
{city_state_zip}

{today_date}

{company_name}
{company_address}

Re: {letter_type}

{dispute_reason}

Account Name: {account_name}
Account Number: XXXX-{account_number}
SSN (Last 4): {ssn_last4}
DOB: {dob}

Sincerely,

{full_name}
"""

            pdf_buffer = generate_pdf_buffer(clean_text)

            st.download_button(
                "📄 Download PDF",
                pdf_buffer,
                file_name="credit_letter.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"Error: {e}")
