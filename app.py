import streamlit as st
from openai import OpenAI
import os
from datetime import date
from io import BytesIO
import re

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
st.markdown("Generate legally structured credit repair letters with professional HTML + properly formatted PDF export.")

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
# PROFESSIONAL PDF GENERATOR
# -----------------------------
def generate_pdf_buffer(
    full_name,
    address,
    city_state_zip,
    today_date,
    company_name,
    company_address,
    letter_type,
    body_html,
    account_name,
    account_number,
    ssn_last4,
    dob
):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=LETTER,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()

    normal_style = ParagraphStyle(
        name="LetterNormal",
        parent=styles["Normal"],
        fontSize=12,
        leading=18,
        spaceAfter=10
    )

    bold_style = ParagraphStyle(
        name="LetterBold",
        parent=styles["Normal"],
        fontSize=12,
        leading=18,
        spaceAfter=14
    )

    story = []

    # Sender
    story.append(Paragraph(full_name, normal_style))
    story.append(Paragraph(address, normal_style))
    story.append(Paragraph(city_state_zip, normal_style))
    story.append(Spacer(1, 0.3 * inch))

    # Date
    story.append(Paragraph(today_date, normal_style))
    story.append(Spacer(1, 0.3 * inch))

    # Company
    story.append(Paragraph(company_name, normal_style))
    story.append(Paragraph(company_address, normal_style))
    story.append(Spacer(1, 0.3 * inch))

    # RE line
    story.append(Paragraph(f"<b>Re: {letter_type}</b>", bold_style))
    story.append(Spacer(1, 0.2 * inch))

    # Convert HTML paragraphs properly
    paragraphs = re.findall(r"<p>(.*?)</p>", body_html, re.DOTALL)

    for p in paragraphs:
        story.append(Paragraph(p.strip(), normal_style))
        story.append(Spacer(1, 0.2 * inch))

    story.append(Spacer(1, 0.3 * inch))

    # Account info
    story.append(Paragraph(f"Account Name: {account_name}", normal_style))
    story.append(Paragraph(f"Account Number: XXXX-{account_number}", normal_style))
    story.append(Paragraph(f"SSN (Last 4): {ssn_last4}", normal_style))
    story.append(Paragraph(f"Date of Birth: {dob}", normal_style))

    story.append(Spacer(1, 0.5 * inch))

    # Signature
    story.append(Paragraph("Sincerely,", normal_style))
    story.append(Spacer(1, 0.7 * inch))
    story.append(Paragraph(full_name, normal_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

# -----------------------------
# GENERATE LETTER
# -----------------------------
if st.button("🚀 Generate Letter"):

    try:
        with st.spinner("Generating legally structured letter..."):

            client = OpenAI(api_key=api_key) if api_key else OpenAI()

            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a professional credit repair legal specialist."},
                    {"role": "user", "content": build_prompt()}
                ]
            )

            body_content = response.choices[0].message.content

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

            # Generate Proper PDF
            pdf_buffer = generate_pdf_buffer(
                full_name,
                address,
                city_state_zip,
                today_date,
                company_name,
                company_address,
                letter_type,
                body_content,
                account_name,
                account_number,
                ssn_last4,
                dob
            )

            st.download_button(
                "📄 Download Professional PDF",
                pdf_buffer,
                file_name="credit_letter.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"Error: {e}")
