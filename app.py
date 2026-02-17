import streamlit as st
from openai import OpenAI
import os
from datetime import date
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import FrameBreak
from reportlab.platypus import PageBreak
from reportlab.platypus import KeepTogether
from reportlab.platypus import ListFlowable, ListItem
from reportlab.platypus import Preformatted
from reportlab.platypus import HRFlowable
from reportlab.platypus import Image
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.platypus import Spacer
from reportlab.platypus import PageTemplate
from reportlab.platypus import BaseDocTemplate
from reportlab.platypus import Frame
from reportlab.platypus import NextPageTemplate
from reportlab.platypus import CondPageBreak
from reportlab.platypus import Flowable
from reportlab.platypus import PageBreak

# Page setup
st.set_page_config(page_title="AI Credit Repair OS", page_icon="💳", layout="wide")

st.title("💳 AI Credit Repair Letter System")
st.markdown("Generate legally structured credit repair letters with HTML + PDF export.")

# Sidebar API
st.sidebar.title("⚙️ AI Settings")
api_key = st.sidebar.text_input("OpenAI API Key (Optional)", type="password", value=os.getenv("OPENAI_API_KEY", ""))
model_name = st.sidebar.selectbox("Model", ["gpt-4.1-mini", "gpt-4.1-nano"], index=0)

# Letter Type Selector
letter_type = st.selectbox(
    "Select Letter Type",
    [
        "Credit Bureau Dispute (FCRA 611)",
        "609 Method of Verification Letter",
        "Debt Validation Letter (FDCPA)",
        "Goodwill Deletion Request",
        "Late Payment Removal Request",
        "Hard Inquiry Removal",
        "Charge-Off Dispute",
        "Identity Theft Dispute"
    ]
)

st.markdown("---")

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
    account_name = st.text_input("Creditor / Furnisher Name")
    account_number = st.text_input("Account Number (Last 4 Only)")
    dispute_reason = st.text_area("Describe Issue")

today_date = date.today().strftime("%B %d, %Y")

# Dynamic Prompt Builder
def build_prompt():
    base = f"""
Write a formal {letter_type}.

Issue: {dispute_reason}
Account: {account_name}
Account Last 4: {account_number}

Use proper legal structure.
Reference FCRA or FDCPA where appropriate.
Be firm, professional, and legally structured.
Return only HTML paragraph tags.
"""
    return base

# HTML TEMPLATE
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
    line-height: 1.6;
}}
.header {{
    margin-bottom: 30px;
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

<div class="section">
<strong>Re: {letter_type}</strong>
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

# PDF Generator
def generate_pdf(text_content, filename):
    doc = SimpleDocTemplate(filename, pagesize=LETTER)
    styles = getSampleStyleSheet()
    story = []

    style = styles["Normal"]
    style.fontSize = 12
    style.leading = 18

    paragraphs = text_content.split("\n")

    for p in paragraphs:
        story.append(Paragraph(p, style))
        story.append(Spacer(1, 0.2 * inch))

    doc.build(story)

# Generate Button
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
                st.download_button("Download HTML", final_html,
                                   file_name="credit_letter.html",
                                   mime="text/html")

            # Clean text for PDF
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

            pdf_path = "/mnt/data/credit_letter.pdf"
            generate_pdf(clean_text, pdf_path)

            st.download_button(
                "📄 Download PDF",
                open(pdf_path, "rb"),
                file_name="credit_letter.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"Error: {e}")
