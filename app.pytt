import streamlit as st
import os
from openai import OpenAI

# -----------------------------
# PAGE CONFIG
st.set_page_config(page_title="AI Landing Page Maker", page_icon="🏗️", layout="wide")

# Custom CSS
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

# -----------------------------
# SIDEBAR CONFIG
st.sidebar.title("⚙️ Configuration")
openai_api_key = st.sidebar.text_input("Ollama API Key (Optional)", type="password", value=os.getenv("OPENAI_API_KEY", ""))
model_name = st.sidebar.selectbox("Model", ["deepseek-coder:latest"], index=0)

st.sidebar.markdown("---")
st.sidebar.title("🎨 Branding")
logo_url = st.sidebar.text_input("Logo URL", value="https://entremotivator.com/wp-content/uploads/2025/12/C948710D-881B-4957-82C2-59F6D6175FD2.png")
brand_name = st.sidebar.text_input("Brand Name", value="AI LANDING PAGES")
primary_color = st.sidebar.color_picker("Primary Color (Header)", "#1a202c")
text_brand_color = st.sidebar.color_picker("Brand Text Color", "#4c51bf")
accent_color = st.sidebar.color_picker("Accent Color (Buttons/Links)", "#e53e3e")

st.sidebar.markdown("---")
st.sidebar.title("🖼️ Visual Assets")
hero_image = st.sidebar.text_input("Hero Image URL", value="https://entremotivator.com/wp-content/uploads/2026/02/IMG_2190-2-scaled.png")
feature_image = st.sidebar.text_input("Feature Image URL", value="https://entremotivator.com/wp-content/uploads/2026/02/C664F277-EC90-42C4-A2C3-CC6CEF855780-2.jpg")

# -----------------------------
# MAIN UI
st.title("🏗️ AI Landing Page Maker")
st.markdown("### Generate high-converting, branded landing pages with AI.")

# Input fields
col1, col2 = st.columns(2)
with col1:
    page_title = st.text_input("Landing Page Title", value="Welcome to Your AI-Powered Landing Page")
    hero_text = st.text_area("Hero Section Text", value="Build fully customized landing pages with AI that match your brand vibe.", height=100)
with col2:
    cta_text = st.text_input("CTA Button Text", value="Get Started Now")
    cta_link = st.text_input("CTA Link", value="https://yourwebsite.com/signup")
    closing_text = st.text_area("Footer Text", value="© 2026 AI Landing Pages. All rights reserved.", height=80)

features_description = st.text_area("Describe key features or sections (AI will generate the content)", 
                                     value="Highlight AI-powered tools, branded hero sections, call-to-actions, testimonials, and visuals for conversions.", height=120)

# HTML Template for Landing Page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title}</title>
<style>
body {{ font-family: Arial, sans-serif; margin:0; padding:0; background-color:#f4f4f4; }}
header {{ background-color: {primary_color}; padding: 40px; text-align:center; color: {text_brand_color}; }}
header img {{ width: 150px; }}
header h1 {{ margin: 20px 0 0 0; }}
section.hero {{ padding: 60px 20px; text-align:center; background: #ffffff; }}
section.hero img {{ max-width: 100%; border-radius: 8px; }}
section.hero p {{ font-size: 18px; margin: 20px 0; }}
a.cta-button {{ display:inline-block; background-color:{accent_color}; color:#fff; padding:15px 30px; text-decoration:none; border-radius:6px; font-weight:bold; }}
section.features {{ padding: 40px 20px; background-color:#fefefe; }}
section.features div {{ margin-bottom:20px; font-size:16px; }}
footer {{ text-align:center; padding:20px; background-color:#ffffff; color:#718096; font-size:12px; }}
</style>
</head>
<body>
<header>
    <img src="{logo_url}" alt="Logo">
    <h1>{brand_name}</h1>
</header>
<section class="hero">
    <img src="{hero_image}" alt="Hero Image">
    <p>{hero_text}</p>
    <a href="{cta_link}" class="cta-button">{cta_text}</a>
</section>
<section class="features">
    {features_content}
    <img src="{feature_image}" alt="Feature Image">
</section>
<footer>
    {closing_text}
</footer>
</body>
</html>
"""

# -----------------------------
# Generate Landing Page
if st.button("🚀 Generate Landing Page"):
    try:
        with st.spinner("AI is crafting your landing page..."):
            # Initialize Ollama/OpenAI client
            if openai_api_key:
                client = OpenAI(api_key=openai_api_key)
            else:
                client = OpenAI()

            # Prompt to generate features/content sections
            system_prompt = f"You are a professional landing page copywriter for {brand_name}. Generate engaging, high-converting content sections for a landing page."
            user_prompt = f"Based on this description: {features_description}, generate 3-4 HTML content blocks using <div> tags. Keep the tone energetic, concise, and branded. Return only HTML."

            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )

            features_content = response.choices[0].message.content

            final_html = HTML_TEMPLATE.format(
                page_title=page_title,
                logo_url=logo_url,
                brand_name=brand_name,
                primary_color=primary_color,
                text_brand_color=text_brand_color,
                accent_color=accent_color,
                hero_image=hero_image,
                hero_text=hero_text,
                cta_link=cta_link,
                cta_text=cta_text,
                features_content=features_content,
                feature_image=feature_image,
                closing_text=closing_text
            )

            st.success("✨ Landing Page Generated Successfully!")

            tab1, tab2 = st.tabs(["👀 Preview", "💻 HTML Code"])

            with tab1:
                st.components.v1.html(final_html, height=900, scrolling=True)

            with tab2:
                st.code(final_html, language="html")
                st.download_button("📥 Download HTML File", final_html, file_name="landing_page.html", mime="text/html")

    except Exception as e:
        st.error(f"An error occurred: {e}")

st.markdown("---")
st.info("💡 Use the sidebar to update branding, colors, and images instantly!")
