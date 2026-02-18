import streamlit as st
import os
import json
from datetime import datetime
from io import BytesIO
import base64

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
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

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

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
st.sidebar.markdown('<p class="section-label">⚙️ Settings</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🎨 Landing Page Generator")
    st.markdown("Create professional landing pages with Divi-compatible WordPress shortcodes and inline CSS.")
    
    st.markdown("---")
    st.markdown("### 📋 How to Use")
    st.markdown("""
    1. Fill in your landing page details
    2. Customize colors to match your brand
    3. Click **Generate Page**
    4. Copy shortcodes to Divi or download HTML
    """)

# ─────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────
st.markdown('<h1 class="main-title">🎨 Divi Landing Page Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Create stunning landing pages with WordPress shortcodes and inline CSS</p>', unsafe_allow_html=True)

# Create two columns for input and preview
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<p class="section-label">📝 Page Content</p>', unsafe_allow_html=True)
    
    page_title = st.text_input(
        "Page Title",
        value="Welcome to Our Service",
        help="Main heading of your landing page"
    )
    
    page_subtitle = st.text_input(
        "Page Subtitle",
        value="Create amazing landing pages with ease",
        help="Secondary heading below the main title"
    )
    
    hero_text = st.text_area(
        "Hero Section Text",
        value="Discover the power of professional landing pages. Our tool helps you create stunning, conversion-focused pages in minutes.",
        height=100,
        help="Main body text for the hero section"
    )
    
    cta_text = st.text_input(
        "CTA Button Text",
        value="Get Started Now",
        help="Text displayed on the call-to-action button"
    )
    
    cta_url = st.text_input(
        "CTA Button URL",
        value="https://example.com/signup",
        help="Where the button should link to"
    )
    
    st.markdown('<p class="section-label">✨ Features</p>', unsafe_allow_html=True)
    
    features_text = st.text_area(
        "Features (one per line)",
        value="✓ Fast & Responsive Design\n✓ SEO Optimized\n✓ Easy to Customize\n✓ Mobile Friendly\n✓ Built-in Analytics",
        height=120,
        help="List your key features, one per line"
    )
    
    features = [f.strip() for f in features_text.split('\n') if f.strip()]

with col2:
    st.markdown('<p class="section-label">🎨 Colors</p>', unsafe_allow_html=True)
    
    col_brand, col_bg, col_text = st.columns(3)
    
    with col_brand:
        brand_color = st.color_picker(
            "Brand Color",
            value="#c9a96e",
            help="Primary brand color"
        )
    
    with col_bg:
        bg_color = st.color_picker(
            "Background Color",
            value="#0f1117",
            help="Page background color"
        )
    
    with col_text:
        text_color = st.color_picker(
            "Text Color",
            value="#f0ede8",
            help="Main text color"
        )
    
    st.markdown('<p class="section-label">📊 Preview</p>', unsafe_allow_html=True)
    
    preview_data = {
        "Title": page_title,
        "Subtitle": page_subtitle,
        "CTA Button": cta_text,
        "CTA URL": cta_url,
        "Features": len(features),
        "Brand Color": brand_color,
        "Background Color": bg_color,
        "Text Color": text_color
    }
    
    for key, value in preview_data.items():
        st.markdown(f"**{key}:** `{value}`")

# ─────────────────────────────────────────
# VALIDATION
# ─────────────────────────────────────────
def validate_inputs():
    errors = []
    if not page_title.strip():
        errors.append("Page Title is required.")
    if not page_subtitle.strip():
        errors.append("Page Subtitle is required.")
    if not hero_text.strip():
        errors.append("Hero Section Text is required.")
    if not cta_text.strip():
        errors.append("CTA Button Text is required.")
    if not cta_url.strip():
        errors.append("CTA Button URL is required.")
    if len(hero_text.strip()) < 20:
        errors.append("Hero text should be at least 20 characters.")
    return errors

# ─────────────────────────────────────────
# GENERATE BUTTON
# ─────────────────────────────────────────
st.markdown("---")

col_generate, col_reset = st.columns(2)

with col_generate:
    generate_btn = st.button("🚀 Generate Landing Page", use_container_width=True)

with col_reset:
    reset_btn = st.button("🔄 Reset Form", use_container_width=True)

if reset_btn:
    st.rerun()

if generate_btn:
    errors = validate_inputs()
    
    if errors:
        st.markdown('<div class="validation-error">', unsafe_allow_html=True)
        for error in errors:
            st.error(error)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.success("✓ Landing page generated successfully!")
        
        # Generate outputs
        shortcodes = generate_divi_shortcodes(page_title, page_subtitle, hero_text, cta_text, cta_url, features, brand_color)
        html = generate_html(page_title, page_subtitle, hero_text, cta_text, cta_url, features, brand_color, bg_color, text_color)
        css = generate_css(brand_color, bg_color, text_color)
        
        # Create tabs for output
        st.markdown("---")
        st.markdown('<p class="section-label">📦 Generated Output</p>', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["📄 HTML Output", "🔗 WordPress Shortcodes", "🎨 Inline CSS"])
        
        with tab1:
            st.markdown("**Complete HTML file with inline CSS:**")
            st.code(html, language="html")
            
            st.download_button(
                label="📥 Download HTML File",
                data=html,
                file_name=f"landing-page-{datetime.now().strftime('%Y%m%d-%H%M%S')}.html",
                mime="text/html",
                use_container_width=True
            )
        
        with tab2:
            st.markdown("**Divi-compatible WordPress shortcodes:**")
            st.markdown("Copy these shortcodes and paste them into your Divi page builder.")
            st.code(shortcodes, language="text")
            
            st.download_button(
                label="📥 Download Shortcodes File",
                data=shortcodes,
                file_name=f"divi-shortcodes-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with tab3:
            st.markdown("**Standalone CSS file:**")
            st.markdown("Use this CSS with your HTML or customize it for your needs.")
            st.code(css, language="css")
            
            st.download_button(
                label="📥 Download CSS File",
                data=css,
                file_name=f"styles-{datetime.now().strftime('%Y%m%d-%H%M%S')}.css",
                mime="text/css",
                use_container_width=True
            )

st.markdown("---")
st.markdown("""
<div class="info-card">
    <strong>💡 Pro Tips:</strong>
    <ul>
        <li>Use the HTML output for standalone landing pages</li>
        <li>Use the shortcodes in Divi for WordPress integration</li>
        <li>Customize the CSS to match your brand guidelines</li>
        <li>Test on mobile devices before publishing</li>
    </ul>
</div>
""", unsafe_allow_html=True)
