import streamlit as st
from openai import OpenAI
import os
from datetime import date

# Page config
st.set_page_config(page_title="AI Credit Letter Generator", page_icon="💳", layout="wide")

# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #f4f6f9;
}
.stButton>button {
    width: 100%;
    height: 3em;
    border-radius: 6px;
    background-color: #1f2937;
    color: white;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #111827;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("⚙️ Settings")
openai_api_key = st.sidebar.text_input("OpenAI API Key (Optional)", type="password", value=os.getenv("OPENAI_API_KEY", ""))
model_name = st.sidebar.selectbox("Model", ["gpt-4.1-mini", "gpt-4.1-nano"], index=0)

st.title("💳 AI Credit Dispute Letter Generator")
st.markdown("Generate professional credit repair and dispute letters instantly.")

# User Information
col1, col2 = st.columns(2)

with col1:
    full_name = st.text_input("Your Full Name")
    address = st.text_input("Street Address")
    city_state_zip = st.text_input("City, State, ZIP")
    ssn_last4 = st.text_input("Last 4 of SSN")
    dob = st.text_input("Date of Birth")

with col2:
    bureau_name = st.selectbox("Credit Bureau",
                               ["Experian", "Equifax", "TransUnion"])
    bureau_address = st.text_area("Bureau Address")
    account_name = st.text_input("Creditor Name")
    account_number = st.text_input("Account Number (Last 4 Only)")
    dispute_reason = st.text_area("Reason for Dispute")

today_date = date.today().strftime("%B %d, %Y")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Credit Dispute Letter</title>
<style>
body {{
    font-family: Arial, sans-serif;
    background-color: #f4f6f9;
    padding: 40px;
}}
.letter-container {{
    background: white;
    padding: 50px;
    max-width: 800px;
    margin: auto;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}}
.header {{
    margin-bottom: 30px;
}}
.section {{
    margin-bottom: 20px;
    line-height: 1.6;
    font-size: 16px;
}}
.signature {{
    margin-top: 40px;
}}
</style>
</head>
<body>
<div class="letter-container">
<div class="header">
<p>{full_name}<br>
{address}<br>
{city_state_zip}</p>

<p>{today_date}</p>

<p>{bureau_name}<br>
{bureau_address}</p>
</div>

<div class="section">
<p><strong>Re: Formal Dispute of Inaccurate Credit Information</strong></p>

{body_content}

<p>Account Name: {account_name}<br>
Account Number: XXXX-{account_number}</p>

<p>SSN (Last 4): {ssn_last4}<br>
Date of Birth: {dob}</p>
</div>

<div class="section">
<p>Please investigate this matter and remove or correct the inaccurate information as required under the Fair Credit Reporting Act (FCRA).</p>
</div>

<div class="signature">
<p>Sincerely,<br><br>
{full_name}</p>
</div>

</div>
</body>
</html>
"""

if st.button("🚀 Generate Credit Letter"):
    try:
        with st.spinner("Generating professional dispute letter..."):

            if openai_api_key:
                client = OpenAI(api_key=openai_api_key)
            else:
                client = OpenAI()

            system_prompt = "You are a professional credit repair specialist. Write formal, legally structured credit dispute letters referencing FCRA."

            user_prompt = f"""
Write a formal credit dispute paragraph explaining the following issue:
{dispute_reason}

Keep it professional, firm, and legally structured.
Return only HTML paragraph tags (<p>).
"""

            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )

            body_content = response.choices[0].message.content

            final_html = HTML_TEMPLATE.format(
                full_name=full_name,
                address=address,
                city_state_zip=city_state_zip,
                today_date=today_date,
                bureau_name=bureau_name,
                bureau_address=bureau_address,
                body_content=body_content,
                account_name=account_name,
                account_number=account_number,
                ssn_last4=ssn_last4,
                dob=dob
            )

            st.success("✅ Credit Dispute Letter Generated!")

            tab1, tab2 = st.tabs(["👀 Preview", "💻 HTML Code"])

            with tab1:
                st.components.v1.html(final_html, height=800, scrolling=True)

            with tab2:
                st.code(final_html, language="html")
                st.download_button("📥 Download Letter", final_html,
                                   file_name="credit_dispute_letter.html",
                                   mime="text/html")

    except Exception as e:
        st.error(f"Error: {e}")
      
