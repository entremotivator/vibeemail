import streamlit as st
from openai import OpenAI
import os

# Set page config
st.set_page_config(page_title="AI Superhero Vibe Tool", page_icon="⚡", layout="wide")

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4c51bf;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #434190;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar for configuration
st.sidebar.title("⚙️ Configuration")
# Note: In this environment, the API key is pre-configured for the allowed models.
# We'll provide an option to override, but default to the system environment.
openai_api_key = st.sidebar.text_input("OpenAI API Key (Optional)", type="password", value=os.getenv("OPENAI_API_KEY", ""))
model_name = st.sidebar.selectbox("Model", ["gpt-4.1-mini", "gpt-4.1-nano", "gemini-2.5-flash"], index=0)

st.sidebar.markdown("---")
st.sidebar.title("🎨 Assets & Branding")
logo_url = st.sidebar.text_input("Logo URL", value="https://entremotivator.com/wp-content/uploads/2025/12/C948710D-881B-4957-82C2-59F6D6175FD2.png")
brand_name = st.sidebar.text_input("Brand Name", value="AI SUPERHEROES")
primary_color = st.sidebar.color_picker("Primary Color (Header)", "#1a202c")
text_brand_color = st.sidebar.color_picker("Brand Text Color", "#4c51bf")
accent_color = st.sidebar.color_picker("Accent Color (Buttons/Links)", "#e53e3e")

st.sidebar.markdown("---")
st.sidebar.title("🖼️ Class Flyers")
flyer_1 = st.sidebar.text_input("Flyer 1 URL", value="https://entremotivator.com/wp-content/uploads/2026/02/IMG_2190-2-scaled.png")
flyer_2 = st.sidebar.text_input("Flyer 2 URL", value="https://entremotivator.com/wp-content/uploads/2026/02/C664F277-EC90-42C4-A2C3-CC6CEF855780-2.jpg")

# Main UI
st.title("⚡ Vibe Tool: Email Generator")
st.markdown("### Create high-converting emails with your unique brand vibe.")

# Input fields for the email content
col1, col2 = st.columns(2)
with col1:
    subject_input = st.text_input("Email Subject", value="⏰ 1 HOUR REMINDER: Building My Own Vibe Tool")
    recipient_name = st.text_input("Recipient Greeting", value="AI Superhero")
    event_time = st.text_input("Event Time", value="Tuesday, Feb 17, 2026 at 6:00 PM EST!")

with col2:
    cta_text = st.text_input("CTA Button Text", value="JOIN THE LIVE CLASS NOW")
    cta_link = st.text_input("CTA Link", value="https://gobrunch.com/events/land/lxgbvm")
    closing_text = st.text_area("Closing Text", value="See you in class!\n— The AI Superhero Team", height=100)

content_description = st.text_area("What is this email about? (AI will generate the body)", 
                                   value="Discover how to create personalized AI tools that match your unique brand 'vibe' and workflow.",
                                   height=100)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{subject}</title>
    <style>
        body, table, td, a {{ -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }}
        table, td {{ mso-table-lspace: 0pt; mso-table-rspace: 0pt; }}
        img {{ -ms-interpolation-mode: bicubic; border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; }}
        a[x-apple-data-detectors] {{ color: inherit !important; text-decoration: none !important; font-size: inherit !important; font-family: inherit !important; font-weight: inherit !important; line-height: inherit !important; }}
        @media screen and (max-width: 600px) {{
            .mobile-padding {{ padding: 20px !important; }}
            .mobile-full-width {{ width: 100% !important; }}
            .mobile-center {{ text-align: center !important; }}
        }}
    </style>
</head>
<body style="margin: 0; padding: 0; background-color: #f4f4f4;">
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;">
        <tr>
            <td align="center" style="padding: 20px 0;">
                <table border="0" cellpadding="0" cellspacing="0" width="600" class="mobile-full-width" style="border-collapse: collapse; background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                    <tr>
                        <td align="center" style="padding: 40px 20px 20px 20px; background-color: {primary_color}; border-top-left-radius: 8px; border-top-right-radius: 8px;">
                            <img src="{logo_url}" alt="Logo" width="150" style="display: block; border: 0;">
                            <h1 style="color: {text_brand_color}; font-family: Arial, sans-serif; font-size: 28px; margin: 10px 0 0 0;">{brand_name}</h1>
                        </td>
                    </tr>
                    <tr>
                        <td align="center" style="padding: 40px 40px 20px 40px;" class="mobile-padding">
                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td align="left" style="color: #333333; font-family: Arial, sans-serif; font-size: 16px; line-height: 24px;">
                                        <p style="margin: 0 0 20px 0;">Hey {recipient_name},</p>
                                        <h2 style="color: {accent_color}; font-family: Arial, sans-serif; font-size: 24px; margin: 0 0 10px 0; text-align: center;">{subject}</h2>
                                        <p style="margin: 0 0 20px 0; font-size: 18px; font-weight: bold; text-align: center;">{event_time}</p>
                                        <div style="margin: 0 0 15px 0;">{body_content}</div>
                                    </td>
                                </tr>
                                <tr>
                                    <td align="center" style="padding: 20px 0;">
                                        <table border="0" cellpadding="0" cellspacing="0">
                                            <tr>
                                                <td align="center" style="border-radius: 6px;" bgcolor="{accent_color}">
                                                    <a href="{cta_link}" target="_blank" style="font-size: 18px; font-family: Arial, sans-serif; color: #ffffff; text-decoration: none; padding: 15px 25px; border-radius: 6px; border: 1px solid {accent_color}; display: inline-block; font-weight: bold;">{cta_text}</a>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td align="center" style="padding: 20px 40px; background-color: #ffffff;">
                            <h3 style="color: #2d3748; font-family: Arial, sans-serif; font-size: 18px; margin: 0 0 15px 0;">🖼️ Class Flyers</h3>
                            <img src="{flyer_1}" alt="Flyer 1" width="520" style="display: block; border: 0; margin-bottom: 20px; border-radius: 8px;">
                            <img src="{flyer_2}" alt="Flyer 2" width="520" style="display: block; border: 0; margin-bottom: 20px; border-radius: 8px;">
                        </td>
                    </tr>
                    <tr>
                        <td align="center" style="padding: 20px 40px 40px 40px; color: #718096; font-family: Arial, sans-serif; font-size: 12px; line-height: 18px;">
                            <div style="white-space: pre-wrap;">{closing_text}</div>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""

if st.button("🚀 Generate Email"):
    try:
        with st.spinner("AI is crafting your email vibe..."):
            # Initialize OpenAI client
            # In this environment, the client will use the pre-configured API key if none is provided
            if openai_api_key:
                client = OpenAI(api_key=openai_api_key)
            else:
                client = OpenAI()
            
            # Create prompt for the body content
            system_prompt = f"You are a professional copywriter for {brand_name}. Your goal is to write energetic, 'superhero' themed email copy."
            user_prompt = f"Write a concise and engaging email body (2-3 paragraphs) based on this description: {content_description}. Return ONLY the HTML-formatted body content (using <p> tags)."
            
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            body_content = response.choices[0].message.content
            
            # Fill the template
            final_html = HTML_TEMPLATE.format(
                subject=subject_input,
                logo_url=logo_url,
                brand_name=brand_name,
                primary_color=primary_color,
                text_brand_color=text_brand_color,
                accent_color=accent_color,
                recipient_name=recipient_name,
                event_time=event_time,
                body_content=body_content,
                cta_link=cta_link,
                cta_text=cta_text,
                flyer_1=flyer_1,
                flyer_2=flyer_2,
                closing_text=closing_text
            )
            
            # Display results
            st.success("✨ Email Generated Successfully!")
            
            tab1, tab2 = st.tabs(["👀 Preview", "💻 HTML Code"])
            
            with tab1:
                st.components.v1.html(final_html, height=800, scrolling=True)
            
            with tab2:
                st.code(final_html, language="html")
                st.download_button("📥 Download HTML File", final_html, file_name="vibe_email.html", mime="text/html")
                
    except Exception as e:
        st.error(f"An error occurred: {e}")

st.markdown("---")
st.info("💡 **Pro Tip:** Use the sidebar to change colors, logos, and flyers to instantly update your brand's vibe!")
