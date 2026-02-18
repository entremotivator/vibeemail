import streamlit as st
import os
import json
from datetime import datetime
from io import BytesIO
import base64
import requests
from openai import OpenAI
import time

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Divi Landing Page Generator",
    page_icon="🎨",
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
.stSelectbox > div > div > div,
.stColorPicker > div > div > input {
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

.code-block {
    background: #0f1117 !important;
    border: 1px solid #2e3245 !important;
    border-radius: 8px !important;
    padding: 1rem !important;
    color: #6ee89a !important;
    font-family: 'Courier New', monospace !important;
    font-size: 0.85rem !important;
    line-height: 1.5 !important;
    overflow-x: auto !important;
}

.preview-frame {
    border: 1px solid #2e3245;
    border-radius: 8px;
    background: #f5f3ef;
    min-height: 600px;
    padding: 0;
    overflow: hidden;
}

.feature-item {
    background: #1a1d27;
    border: 1px solid #2e3245;
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
}

.feature-item input {
    flex: 1;
    background: #0f1117 !important;
    border: 1px solid #2e3245 !important;
    padding: 8px 12px !important;
    border-radius: 6px !important;
    color: #f0ede8 !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def generate_with_llm(prompt, api_key, model="gpt-4o-mini", max_tokens=2000):
    """Generate content using OpenAI API"""
    
    if not api_key:
        st.error("❌ OpenAI API key is required. Add it in the sidebar.")
        return None
    
    try:
        client = OpenAI(api_key=api_key)
        
        response = client.messages.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=max_tokens
        )
        
        return response.content[0].text
    
    except Exception as e:
        st.error(f"❌ OpenAI API Error: {str(e)}")
        return None

def generate_landing_page_content(business_description, api_key, model="gpt-4o-mini"):
    """Generate complete landing page content using LLM"""
    
    prompt = f"""You are a professional copywriter and landing page expert. Create a complete, compelling landing page for the following business:

Business Description: {business_description}

Generate the following in JSON format:
{{
    "title": "A powerful, concise main headline (5-10 words)",
    "subtitle": "An engaging subheading that complements the title (10-15 words)",
    "hero_text": "A compelling hero section paragraph (150-250 words) that explains the value proposition, benefits, and why customers should care",
    "features": [
        "Feature 1 with detailed description (15-25 words)",
        "Feature 2 with detailed description (15-25 words)",
        "Feature 3 with detailed description (15-25 words)",
        "Feature 4 with detailed description (15-25 words)",
        "Feature 5 with detailed description (15-25 words)",
        "Feature 6 with detailed description (15-25 words)"
    ],
    "cta_text": "A compelling call-to-action button text (2-4 words)",
    "cta_description": "A brief description of what happens after clicking (20-30 words)"
}}

Make the content persuasive, professional, and conversion-focused. Use power words and psychological triggers."""
    
    content = generate_with_llm(prompt, api_key, model, max_tokens=2500)
    
    if content:
        try:
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
    
    return None

def generate_divi_shortcodes(title, subtitle, hero_text, cta_text, cta_url, features, brand_color):
    """Generate Divi-compatible WordPress shortcodes"""
    
    shortcodes = f"""<!-- Divi Landing Page Shortcodes -->
<!-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -->

[et_pb_section fullwidth="off" specialty="off"]
  [et_pb_row]
    [et_pb_column type="4_4"]

      <!-- HERO SECTION -->
      [et_pb_text]
        <h1 style="color: {brand_color}; font-size: 3em; margin-bottom: 20px; font-family: 'DM Serif Display', serif;">{title}</h1>
        <h2 style="color: #8a8f9e; font-size: 1.5em; margin-bottom: 30px; font-weight: 300;">{subtitle}</h2>
        <p style="font-size: 1.1em; line-height: 1.8; margin-bottom: 30px; color: #f0ede8;">{hero_text}</p>
      [/et_pb_text]

      <!-- CALL-TO-ACTION BUTTON -->
      [et_pb_button 
        button_text="{cta_text}" 
        button_alignment="left" 
        button_text_color="{brand_color}" 
        button_bg_color="#ffffff" 
        button_border_color="{brand_color}" 
        url="{cta_url}" 
        button_text_size="18px" 
        button_letter_spacing="2px" 
        button_font="DM Sans|600||on|||||" 
        button_use_icon="off" 
        button_border_width="2px" 
        button_border_radius="8px" 
        button_letter_spacing_hover="2px" 
        button_text_color_hover="#ffffff" 
        button_bg_color_hover="{brand_color}"
      ]
      [/et_pb_button]
"""

    if features:
        shortcodes += f"""
      <!-- FEATURES SECTION -->
      [et_pb_text]
        <h3 style="color: {brand_color}; margin-top: 60px; margin-bottom: 30px; font-family: 'DM Serif Display', serif;">Why Choose Us</h3>
      [/et_pb_text]

      [et_pb_row column_structure="1_3,1_3,1_3"]
"""
        for i, feature in enumerate(features[:3]):
            shortcodes += f"""        [et_pb_column type="1_3"]
          [et_pb_text]
            <div style="text-align: center; padding: 20px; border: 1px solid {brand_color}; border-radius: 8px; background: rgba({hex_to_rgb(brand_color)[0]}, {hex_to_rgb(brand_color)[1]}, {hex_to_rgb(brand_color)[2]}, 0.05);">
              <p style="color: {brand_color}; font-weight: bold; font-size: 1.1em;">{feature}</p>
            </div>
          [/et_pb_text]
        [/et_pb_column]
"""
        shortcodes += """      [/et_pb_row]
"""

        if len(features) > 3:
            shortcodes += """
      [et_pb_row column_structure="1_3,1_3,1_3"]
"""
            for feature in features[3:6]:
                shortcodes += f"""        [et_pb_column type="1_3"]
          [et_pb_text]
            <div style="text-align: center; padding: 20px; border: 1px solid {brand_color}; border-radius: 8px; background: rgba({hex_to_rgb(brand_color)[0]}, {hex_to_rgb(brand_color)[1]}, {hex_to_rgb(brand_color)[2]}, 0.05);">
              <p style="color: {brand_color}; font-weight: bold; font-size: 1.1em;">{feature}</p>
            </div>
          [/et_pb_text]
        [/et_pb_column]
"""
            shortcodes += """      [/et_pb_row]
"""

    shortcodes += """
    [/et_pb_column]
  [/et_pb_row]
[/et_pb_section]
"""
    return shortcodes

def generate_html(title, subtitle, hero_text, cta_text, cta_url, features, brand_color, bg_color, text_color):
    """Generate complete HTML with inline CSS"""
    
    rgb = hex_to_rgb(brand_color)
    rgb_str = f"{rgb[0]}, {rgb[1]}, {rgb[2]}"
    
    features_html = ""
    if features:
        features_html = f"""
    <div class="features-section">
        <div class="container">
            <h3>Why Choose Us</h3>
            <div class="features-grid">
"""
        for feature in features:
            features_html += f"""                <div class="feature-card">
                    <p>{feature}</p>
                </div>
"""
        features_html += """            </div>
        </div>
    </div>
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background-color: {bg_color};
            color: {text_color};
            line-height: 1.6;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}

        .hero-section {{
            padding: 80px 20px;
            text-align: center;
        }}

        .hero-section h1 {{
            font-family: 'DM Serif Display', serif;
            font-size: 3.5rem;
            margin-bottom: 20px;
            color: {brand_color};
            font-weight: 700;
            letter-spacing: -1px;
        }}

        .hero-section h2 {{
            font-size: 1.5rem;
            margin-bottom: 30px;
            color: #8a8f9e;
            font-weight: 300;
        }}

        .hero-section p {{
            font-size: 1.1rem;
            margin-bottom: 40px;
            color: {text_color};
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.8;
        }}

        .cta-button {{
            display: inline-block;
            padding: 16px 40px;
            background-color: {brand_color};
            color: {bg_color};
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1rem;
            letter-spacing: 0.05em;
            transition: all 0.3s ease;
            border: 2px solid {brand_color};
            text-transform: uppercase;
        }}

        .cta-button:hover {{
            background-color: transparent;
            color: {brand_color};
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba({rgb_str}, 0.3);
        }}

        .features-section {{
            padding: 80px 20px;
            background-color: rgba({rgb_str}, 0.05);
            margin-top: 60px;
        }}

        .features-section h3 {{
            font-family: 'DM Serif Display', serif;
            font-size: 2.5rem;
            margin-bottom: 60px;
            text-align: center;
            color: {brand_color};
        }}

        .features-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
        }}

        .feature-card {{
            padding: 30px;
            border: 1px solid {brand_color};
            border-radius: 8px;
            background: rgba({rgb_str}, 0.05);
            text-align: center;
            transition: all 0.3s ease;
        }}

        .feature-card:hover {{
            border-color: {brand_color};
            background: rgba({rgb_str}, 0.1);
            transform: translateY(-5px);
        }}

        .feature-card p {{
            color: {brand_color};
            font-weight: 600;
            font-size: 1.1rem;
            line-height: 1.6;
        }}

        @media (max-width: 768px) {{
            .hero-section h1 {{
                font-size: 2.5rem;
            }}

            .hero-section h2 {{
                font-size: 1.2rem;
            }}

            .features-section h3 {{
                font-size: 2rem;
            }}

            .features-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="hero-section">
        <div class="container">
            <h1>{title}</h1>
            <h2>{subtitle}</h2>
            <p>{hero_text}</p>
            <a href="{cta_url}" class="cta-button">{cta_text}</a>
        </div>
    </div>
{features_html}
</body>
</html>"""
    
    return html

def generate_css(brand_color, bg_color, text_color):
    """Generate standalone CSS file"""
    
    rgb = hex_to_rgb(brand_color)
    rgb_str = f"{rgb[0]}, {rgb[1]}, {rgb[2]}"
    
    css = f"""/* Generated Landing Page CSS */
/* Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} */

:root {{
    --brand-color: {brand_color};
    --bg-color: {bg_color};
    --text-color: {text_color};
    --secondary-text: #8a8f9e;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    line-height: 1.6;
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}}

.hero-section {{
    padding: 80px 20px;
    text-align: center;
}}

.hero-section h1 {{
    font-family: 'DM Serif Display', serif;
    font-size: 3.5rem;
    margin-bottom: 20px;
    color: var(--brand-color);
    font-weight: 700;
    letter-spacing: -1px;
}}

.hero-section h2 {{
    font-size: 1.5rem;
    margin-bottom: 30px;
    color: var(--secondary-text);
    font-weight: 300;
}}

.hero-section p {{
    font-size: 1.1rem;
    margin-bottom: 40px;
    color: var(--text-color);
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.8;
}}

.cta-button {{
    display: inline-block;
    padding: 16px 40px;
    background-color: var(--brand-color);
    color: var(--bg-color);
    text-decoration: none;
    border-radius: 8px;
    font-weight: 600;
    font-size: 1rem;
    letter-spacing: 0.05em;
    transition: all 0.3s ease;
    border: 2px solid var(--brand-color);
    text-transform: uppercase;
}}

.cta-button:hover {{
    background-color: transparent;
    color: var(--brand-color);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba({rgb_str}, 0.3);
}}

.features-section {{
    padding: 80px 20px;
    background-color: rgba({rgb_str}, 0.05);
    margin-top: 60px;
}}

.features-section h3 {{
    font-family: 'DM Serif Display', serif;
    font-size: 2.5rem;
    margin-bottom: 60px;
    text-align: center;
    color: var(--brand-color);
}}

.features-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 30px;
}}

.feature-card {{
    padding: 30px;
    border: 1px solid var(--brand-color);
    border-radius: 8px;
    background: rgba({rgb_str}, 0.05);
    text-align: center;
    transition: all 0.3s ease;
}}

.feature-card:hover {{
    border-color: var(--brand-color);
    background: rgba({rgb_str}, 0.1);
    transform: translateY(-5px);
}}

.feature-card p {{
    color: var(--brand-color);
    font-weight: 600;
    font-size: 1.1em;
    line-height: 1.6;
}}

@media (max-width: 768px) {{
    .hero-section h1 {{
        font-size: 2.5rem;
    }}

    .hero-section h2 {{
        font-size: 1.2rem;
    }}

    .features-section h3 {{
        font-size: 2rem;
    }}

    .features-grid {{
        grid-template-columns: 1fr;
    }}
}}
"""
    return css

def publish_to_wordpress(wp_url, wp_username, wp_password, page_title, page_content, shortcodes):
    """Publish landing page to WordPress using REST API"""
    
    if not all([wp_url, wp_username, wp_password]):
        st.error("❌ WordPress credentials are required. Add them in the sidebar.")
        return False
    
    try:
        api_endpoint = f"{wp_url.rstrip('/')}/wp-json/wp/v2/pages"
        
        auth_string = f"{wp_username}:{wp_password}"
        auth_bytes = auth_string.encode('utf-8')
        auth_b64 = base64.b64encode(auth_bytes).decode('utf-8')
        
        headers = {
            "Authorization": f"Basic {auth_b64}",
            "Content-Type": "application/json"
        }
        
        full_content = f"{page_content}\n\n{shortcodes}"
        
        payload = {
            "title": page_title,
            "content": full_content,
            "status": "draft",
            "comment_status": "closed"
        }
        
        with st.spinner("📤 Publishing to WordPress..."):
            response = requests.post(api_endpoint, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 201:
            page_data = response.json()
            page_id = page_data.get('id')
            page_link = page_data.get('link')
            st.success(f"✅ Page published successfully!\n\n**Page ID:** {page_id}\n\n**Link:** {page_link}")
            return True
        else:
            st.error(f"❌ WordPress Error: {response.status_code} - {response.text}")
            return False
    
    except Exception as e:
        st.error(f"❌ WordPress Connection Error: {str(e)}")
        return False

# ─────────────────────────────────────────
# SIDEBAR - OPENAI & WORDPRESS CONFIG
# ─────────────────────────────────────────
st.sidebar.markdown('<p class="section-label">⚙️ Configuration</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🎨 AI Landing Page Generator")
    st.markdown("Create professional landing pages with AI-generated content, live preview, and WordPress integration.")
    
    # OpenAI Configuration
    st.markdown("---")
    st.markdown("### 🤖 OpenAI API Setup")
    
    openai_api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Get your API key from https://platform.openai.com/api-keys"
    )
    
    ai_model = st.selectbox(
        "AI Model",
        ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
        help="Choose the AI model for content generation"
    )
    
    # WordPress Configuration
    st.markdown("---")
    st.markdown("### 📱 WordPress API Setup")
    
    wp_url = st.text_input(
        "WordPress Site URL",
        placeholder="https://example.com",
        help="Your WordPress site URL"
    )
    
    wp_username = st.text_input(
        "WordPress Username",
        help="Your WordPress admin username"
    )
    
    wp_password = st.text_input(
        "WordPress Password",
        type="password",
        help="Your WordPress password or Application Password"
    )
    
    st.markdown("---")
    st.markdown("### 📋 How to Use")
    st.markdown("""
    1. **Enter business description**
    2. **Click "Generate with AI"** to create all content
    3. **Edit features** in the main panel
    4. **View live preview** on the right
    5. **Export or publish** to WordPress
    """)

# ─────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────
st.markdown('<h1 class="main-title">🎨 AI Landing Page Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Create stunning landing pages with AI, live preview, and WordPress integration</p>', unsafe_allow_html=True)

# Initialize session state
if 'page_title' not in st.session_state:
    st.session_state.page_title = ""
if 'page_subtitle' not in st.session_state:
    st.session_state.page_subtitle = ""
if 'hero_text' not in st.session_state:
    st.session_state.hero_text = ""
if 'features' not in st.session_state:
    st.session_state.features = []
if 'cta_text' not in st.session_state:
    st.session_state.cta_text = ""
if 'cta_url' not in st.session_state:
    st.session_state.cta_url = ""
if 'brand_color' not in st.session_state:
    st.session_state.brand_color = "#c9a96e"
if 'bg_color' not in st.session_state:
    st.session_state.bg_color = "#0f1117"
if 'text_color' not in st.session_state:
    st.session_state.text_color = "#f0ede8"

# Business Description Input
st.markdown('<p class="section-label">📝 Business Description</p>', unsafe_allow_html=True)

business_description = st.text_area(
    "Describe your business or service",
    placeholder="E.g., A SaaS tool for project management that helps teams collaborate better...",
    height=100,
    help="Provide details about your business, target audience, and unique value proposition"
)

# Generate with AI Button
col_gen, col_space = st.columns([1, 3])

with col_gen:
    if st.button("🤖 Generate with AI", use_container_width=True):
        if not business_description.strip():
            st.error("❌ Please enter a business description first.")
        elif not openai_api_key:
            st.error("❌ Please add your OpenAI API key in the sidebar.")
        else:
            with st.spinner("🤖 Generating landing page content..."):
                content = generate_landing_page_content(business_description, openai_api_key, ai_model)
                
                if content:
                    st.session_state.page_title = content.get('title', '')
                    st.session_state.page_subtitle = content.get('subtitle', '')
                    st.session_state.hero_text = content.get('hero_text', '')
                    st.session_state.features = content.get('features', [])
                    st.session_state.cta_text = content.get('cta_text', 'Get Started')
                    st.session_state.cta_url = "https://example.com/signup"
                    st.success("✅ Content generated successfully!")
                    st.rerun()

st.markdown("---")

# Main Content Area with Live Preview
col_edit, col_preview = st.columns([1, 1])

with col_edit:
    st.markdown('<p class="section-label">✏️ Edit Content</p>', unsafe_allow_html=True)
    
    st.session_state.page_title = st.text_input(
        "Page Title",
        value=st.session_state.page_title,
        key="title_input"
    )
    
    st.session_state.page_subtitle = st.text_input(
        "Page Subtitle",
        value=st.session_state.page_subtitle,
        key="subtitle_input"
    )
    
    st.session_state.hero_text = st.text_area(
        "Hero Section Text",
        value=st.session_state.hero_text,
        height=120,
        key="hero_input"
    )
    
    st.session_state.cta_text = st.text_input(
        "CTA Button Text",
        value=st.session_state.cta_text,
        key="cta_text_input"
    )
    
    st.session_state.cta_url = st.text_input(
        "CTA Button URL",
        value=st.session_state.cta_url,
        key="cta_url_input"
    )
    
    st.markdown('<p class="section-label">✨ Features (Edit & Add)</p>', unsafe_allow_html=True)
    
    # Display and edit features
    for i, feature in enumerate(st.session_state.features):
        col_feat, col_del = st.columns([10, 1])
        
        with col_feat:
            st.session_state.features[i] = st.text_input(
                f"Feature {i+1}",
                value=feature,
                key=f"feature_{i}",
                label_visibility="collapsed"
            )
        
        with col_del:
            if st.button("🗑️", key=f"del_{i}", help="Delete feature"):
                st.session_state.features.pop(i)
                st.rerun()
    
    # Add new feature button
    if st.button("➕ Add Feature", use_container_width=True):
        st.session_state.features.append("")
        st.rerun()
    
    st.markdown("---")
    st.markdown('<p class="section-label">🎨 Colors</p>', unsafe_allow_html=True)
    
    col_brand, col_bg, col_text = st.columns(3)
    
    with col_brand:
        st.session_state.brand_color = st.color_picker(
            "Brand Color",
            value=st.session_state.brand_color,
            key="brand_color_picker"
        )
    
    with col_bg:
        st.session_state.bg_color = st.color_picker(
            "Background Color",
            value=st.session_state.bg_color,
            key="bg_color_picker"
        )
    
    with col_text:
        st.session_state.text_color = st.color_picker(
            "Text Color",
            value=st.session_state.text_color,
            key="text_color_picker"
        )

with col_preview:
    st.markdown('<p class="section-label">👁️ Live Preview</p>', unsafe_allow_html=True)
    
    # Generate HTML for preview
    if st.session_state.page_title:
        html_content = generate_html(
            st.session_state.page_title,
            st.session_state.page_subtitle,
            st.session_state.hero_text,
            st.session_state.cta_text,
            st.session_state.cta_url,
            st.session_state.features,
            st.session_state.brand_color,
            st.session_state.bg_color,
            st.session_state.text_color
        )
        
        # Display preview in iframe
        st.components.v1.html(html_content, height=700, scrolling=True)
    else:
        st.info("👈 Fill in the content on the left to see a live preview here")

# ─────────────────────────────────────────
# EXPORT & PUBLISH SECTION
# ─────────────────────────────────────────
st.markdown("---")
st.markdown('<p class="section-label">📦 Export & Publish</p>', unsafe_allow_html=True)

col_export1, col_export2, col_export3, col_export4 = st.columns(4)

if st.session_state.page_title:
    # Generate all outputs
    shortcodes = generate_divi_shortcodes(
        st.session_state.page_title,
        st.session_state.page_subtitle,
        st.session_state.hero_text,
        st.session_state.cta_text,
        st.session_state.cta_url,
        st.session_state.features,
        st.session_state.brand_color
    )
    
    html = generate_html(
        st.session_state.page_title,
        st.session_state.page_subtitle,
        st.session_state.hero_text,
        st.session_state.cta_text,
        st.session_state.cta_url,
        st.session_state.features,
        st.session_state.brand_color,
        st.session_state.bg_color,
        st.session_state.text_color
    )
    
    css = generate_css(st.session_state.brand_color, st.session_state.bg_color, st.session_state.text_color)
    
    with col_export1:
        st.download_button(
            label="📥 HTML",
            data=html,
            file_name=f"landing-page-{datetime.now().strftime('%Y%m%d-%H%M%S')}.html",
            mime="text/html",
            use_container_width=True
        )
    
    with col_export2:
        st.download_button(
            label="📥 Shortcodes",
            data=shortcodes,
            file_name=f"shortcodes-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col_export3:
        st.download_button(
            label="📥 CSS",
            data=css,
            file_name=f"styles-{datetime.now().strftime('%Y%m%d-%H%M%S')}.css",
            mime="text/css",
            use_container_width=True
        )
    
    with col_export4:
        if st.button("📤 Publish to WP", use_container_width=True):
            page_content = f"""<h1>{st.session_state.page_title}</h1>
<h2>{st.session_state.page_subtitle}</h2>
<p>{st.session_state.hero_text}</p>
<p><a href="{st.session_state.cta_url}" class="button">{st.session_state.cta_text}</a></p>"""
            
            publish_to_wordpress(
                wp_url,
                wp_username,
                wp_password,
                st.session_state.page_title,
                page_content,
                shortcodes
            )
    
    # Show code tabs
    st.markdown("---")
    st.markdown('<p class="section-label">💻 Code</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📄 HTML", "🔗 Shortcodes", "🎨 CSS"])
    
    with tab1:
        st.code(html, language="html")
    
    with tab2:
        st.code(shortcodes, language="text")
    
    with tab3:
        st.code(css, language="css")

else:
    st.info("👈 Generate content with AI or fill in the details to export")

st.markdown("---")
st.markdown("""
<div class="info-card">
    <strong>💡 Pro Tips:</strong>
    <ul>
        <li>Use AI generation for faster content creation</li>
        <li>Edit features directly in the list</li>
        <li>Watch the live preview update as you type</li>
        <li>Download HTML for standalone pages</li>
        <li>Use shortcodes in Divi for WordPress</li>
        <li>Publish directly to WordPress with one click</li>
    </ul>
</div>
""", unsafe_allow_html=True)
