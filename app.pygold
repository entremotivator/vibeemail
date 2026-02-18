import streamlit as st
import json
import re
import time
from datetime import datetime
import base64

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="PageForge — AI Landing Page Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Syne:wght@400;500;600;700;800&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');

:root {
    --bg: #07080f;
    --surface: #0e1019;
    --surface2: #141622;
    --border: #1e2133;
    --accent: #ff3c5f;
    --accent2: #ff7a4d;
    --blue: #4d7cff;
    --gold: #ffc44d;
    --text: #e8eaf0;
    --muted: #5a5f7a;
    --success: #36d37e;
}

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}

.stApp {
    background: var(--bg) !important;
}

/* HIDE streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
    width: 320px !important;
}

section[data-testid="stSidebar"] > div {
    padding: 0 !important;
}

/* TYPOGRAPHY */
h1, h2, h3 {
    font-family: 'Bebas Neue', sans-serif !important;
    letter-spacing: 0.05em !important;
    color: var(--text) !important;
}

/* INPUTS */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.875rem !important;
    caret-color: var(--accent) !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(255, 60, 95, 0.15) !important;
    outline: none !important;
}

label, .stTextInput label, .stTextArea label, .stSelectbox label {
    color: var(--muted) !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-family: 'Space Mono', monospace !important;
}

/* BUTTONS - Primary */
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.875rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    padding: 0.65rem 1.5rem !important;
    border: none !important;
    border-radius: 6px !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
    width: 100%;
}

.stButton > button:hover {
    background: #ff5571 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(255,60,95,0.4) !important;
}

/* DOWNLOAD BUTTONS */
.stDownloadButton > button {
    background: var(--surface2) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    padding: 0.6rem 1rem !important;
    width: 100%;
    transition: all 0.15s ease !important;
}

.stDownloadButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    background: rgba(255,60,95,0.05) !important;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 4px !important;
    gap: 2px !important;
}

.stTabs [data-baseweb="tab"] {
    color: var(--muted) !important;
    border-radius: 6px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    padding: 0.5rem 1rem !important;
}

.stTabs [aria-selected="true"] {
    background: var(--accent) !important;
    color: #fff !important;
    font-weight: 700 !important;
}

/* SELECTBOX */
.stSelectbox [data-baseweb="select"] > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
}

/* COLOR PICKERS */
.stColorPicker > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
}

/* SLIDERS */
.stSlider > div > div > div > div {
    background: var(--accent) !important;
}

/* CODE BLOCKS */
.stCodeBlock {
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

/* CHECKBOX */
.stCheckbox > label > div {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
}

/* ALERTS */
.stSuccess > div {
    background: rgba(54,211,126,0.1) !important;
    border: 1px solid rgba(54,211,126,0.3) !important;
    border-radius: 8px !important;
    color: var(--success) !important;
}

.stError > div {
    background: rgba(255,60,95,0.1) !important;
    border: 1px solid rgba(255,60,95,0.3) !important;
    border-radius: 8px !important;
    color: #ff6b85 !important;
}

.stInfo > div {
    background: rgba(77,124,255,0.1) !important;
    border: 1px solid rgba(77,124,255,0.3) !important;
    border-radius: 8px !important;
    color: #7a9fff !important;
}

/* EXPANDER */
.streamlit-expanderHeader {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
}

/* CUSTOM COMPONENTS */
.forge-header {
    padding: 2rem 2rem 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 0;
    background: linear-gradient(180deg, rgba(255,60,95,0.04) 0%, transparent 100%);
}

.forge-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    letter-spacing: 0.08em;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.25rem;
}

.forge-logo span {
    color: var(--accent);
}

.forge-tagline {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: var(--muted);
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

.section-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(255,60,95,0.1);
    border: 1px solid rgba(255,60,95,0.25);
    border-radius: 4px;
    padding: 0.2rem 0.6rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 1rem;
}

.section-chip.blue {
    background: rgba(77,124,255,0.1);
    border-color: rgba(77,124,255,0.25);
    color: var(--blue);
}

.section-chip.gold {
    background: rgba(255,196,77,0.1);
    border-color: rgba(255,196,77,0.25);
    color: var(--gold);
}

.section-chip.success {
    background: rgba(54,211,126,0.1);
    border-color: rgba(54,211,126,0.25);
    color: var(--success);
}

.stat-row {
    display: flex;
    gap: 0.75rem;
    margin: 1rem 0;
}

.stat-box {
    flex: 1;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.75rem;
    text-align: center;
}

.stat-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    color: var(--accent);
    letter-spacing: 0.05em;
    line-height: 1;
}

.stat-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.25rem;
}

.feature-row {
    display: flex;
    gap: 8px;
    margin-bottom: 8px;
    align-items: center;
}

.step-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.5rem;
    color: rgba(255,60,95,0.15);
    line-height: 1;
    min-width: 2rem;
}

.tip-block {
    background: rgba(77,124,255,0.06);
    border-left: 3px solid var(--blue);
    border-radius: 0 6px 6px 0;
    padding: 0.75rem 1rem;
    margin: 0.75rem 0;
    font-size: 0.8rem;
    color: #8aacff;
    line-height: 1.6;
}

.preview-toolbar {
    display: flex;
    align-items: center;
    gap: 8px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px 8px 0 0;
    padding: 0.5rem 0.75rem;
    border-bottom: none;
}

.preview-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
}

.preview-url {
    flex: 1;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 0.2rem 0.6rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: var(--muted);
    margin-left: 0.5rem;
}

.theme-card {
    background: var(--surface2);
    border: 2px solid var(--border);
    border-radius: 8px;
    padding: 0.75rem;
    cursor: pointer;
    transition: all 0.15s ease;
    text-align: center;
}

.theme-card:hover {
    border-color: var(--accent);
}

.theme-card.active {
    border-color: var(--accent);
    background: rgba(255,60,95,0.08);
}

.export-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.export-card-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1rem;
    letter-spacing: 0.08em;
    color: var(--text);
}

.export-card-desc {
    font-size: 0.75rem;
    color: var(--muted);
    line-height: 1.5;
    margin-bottom: 0.5rem;
}

hr.forge-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.25rem 0;
}

.main-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3rem;
    letter-spacing: 0.06em;
    color: var(--text);
    line-height: 1;
    margin-bottom: 0.2rem;
}

.main-title .accent { color: var(--accent); }

.toolbar {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.6rem 1rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    margin-bottom: 1.25rem;
}

.toolbar-item {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--muted);
    padding: 0.25rem 0.6rem;
    border-radius: 4px;
    cursor: pointer;
}

.toolbar-item.active {
    background: rgba(255,60,95,0.15);
    color: var(--accent);
}

.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.6rem;
    display: block;
}

.accordion-header {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.875rem;
    color: var(--text);
}

.stNumberInput > div > div > input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
    font-family: 'Space Mono', monospace !important;
}

.stRadio > div {
    gap: 0.5rem;
}

.stRadio [data-testid="stMarkdownContainer"] p {
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.875rem !important;
}

/* Progress bar */
.stProgress > div > div {
    background: var(--accent) !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def generate_with_openai(prompt, api_key, model="gpt-4o", max_tokens=4000, system=None):
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.8,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"❌ OpenAI Error: {str(e)}")
        return None

def generate_all_content(description, tone, industry, audience, api_key, model):
    system = """You are an elite conversion copywriter and landing page strategist. 
    You create high-converting, psychologically compelling landing page content.
    Always respond with valid JSON only. No markdown, no extra text."""
    
    prompt = f"""Create a complete, conversion-optimized landing page for:

BUSINESS: {description}
TONE: {tone}
INDUSTRY: {industry}
TARGET AUDIENCE: {audience}

Return ONLY this JSON structure:
{{
  "headline": "Short punchy headline, max 8 words, use power words",
  "subheadline": "1-sentence value prop with specificity, 12-20 words",
  "hero_body": "2-3 sentence emotional hook that speaks to pain points and dreams, 50-80 words",
  "cta_primary": "2-4 word action button text",
  "cta_secondary": "2-4 word secondary action",
  "features": [
    {{"icon": "⚡", "title": "Feature Title", "desc": "25-35 word compelling benefit description"}},
    {{"icon": "🎯", "title": "Feature Title", "desc": "25-35 word compelling benefit description"}},
    {{"icon": "🔥", "title": "Feature Title", "desc": "25-35 word compelling benefit description"}},
    {{"icon": "💎", "title": "Feature Title", "desc": "25-35 word compelling benefit description"}},
    {{"icon": "🚀", "title": "Feature Title", "desc": "25-35 word compelling benefit description"}},
    {{"icon": "✨", "title": "Feature Title", "desc": "25-35 word compelling benefit description"}}
  ],
  "testimonials": [
    {{"name": "First Last", "role": "Job Title, Company", "text": "30-40 word glowing testimonial with specific result", "rating": 5}},
    {{"name": "First Last", "role": "Job Title, Company", "text": "30-40 word glowing testimonial with specific result", "rating": 5}},
    {{"name": "First Last", "role": "Job Title, Company", "text": "30-40 word glowing testimonial with specific result", "rating": 5}}
  ],
  "faq": [
    {{"q": "Common objection as question?", "a": "35-45 word reassuring answer"}},
    {{"q": "Another key concern?", "a": "35-45 word reassuring answer"}},
    {{"q": "Pricing or commitment question?", "a": "35-45 word reassuring answer"}},
    {{"q": "Results or timeline question?", "a": "35-45 word reassuring answer"}}
  ],
  "stats": [
    {{"num": "10k+", "label": "Happy Customers"}},
    {{"num": "98%", "label": "Satisfaction Rate"}},
    {{"num": "3x", "label": "Average ROI"}},
    {{"num": "24/7", "label": "Support"}}
  ],
  "nav_links": ["Features", "Testimonials", "Pricing", "FAQ"],
  "brand_name": "Short brand/company name",
  "tagline": "Short 3-6 word brand tagline",
  "footer_text": "1 sentence footer tagline",
  "email_placeholder": "your@email.com",
  "social_proof": "X companies / X users / X downloads — brief social proof line"
}}"""
    
    content = generate_with_openai(prompt, api_key, model, 4000, system)
    if content:
        try:
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            st.error(f"JSON parse error: {e}")
    return None

def generate_section_content(section_type, context, api_key, model):
    """Regenerate a specific section"""
    system = "You are an elite copywriter. Return only valid JSON, no extra text."
    
    prompts = {
        "headline": f"Write 3 alternative powerful headlines for: {context}. Return: {{\"options\": [\"headline1\", \"headline2\", \"headline3\"]}}",
        "cta": f"Write 5 compelling CTA button texts for: {context}. Return: {{\"options\": [\"cta1\", \"cta2\", \"cta3\", \"cta4\", \"cta5\"]}}",
        "features": f"Write 6 compelling product features for: {context}. Return: {{\"features\": [{{\"icon\":\"⚡\",\"title\":\"T\",\"desc\":\"D\"}}, ...]}}",
    }
    
    content = generate_with_openai(prompts.get(section_type, ""), api_key, model, 1500, system)
    if content:
        try:
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
    return None

def generate_complete_html(data, settings):
    """Generate a full, beautiful, standalone HTML landing page"""
    
    s = settings
    brand_color = s.get('brand_color', '#6c63ff')
    accent_color = s.get('accent_color', '#ff6584')
    bg_color = s.get('bg_color', '#ffffff')
    text_color = s.get('text_color', '#1a1a2e')
    font_pair = s.get('font_pair', 'Modern')
    layout_style = s.get('layout_style', 'Standard')
    nav_sticky = s.get('nav_sticky', True)
    show_testimonials = s.get('show_testimonials', True)
    show_faq = s.get('show_faq', True)
    show_stats = s.get('show_stats', True)
    show_cta_banner = s.get('show_cta_banner', True)
    show_nav = s.get('show_nav', True)
    cta_url = s.get('cta_url', '#signup')
    animation_style = s.get('animation_style', 'Smooth')
    hero_layout = s.get('hero_layout', 'Centered')
    
    brand_rgb = hex_to_rgb(brand_color)
    accent_rgb = hex_to_rgb(accent_color)
    bg_rgb = hex_to_rgb(bg_color)
    
    # Determine if dark background
    is_dark = (bg_rgb[0] + bg_rgb[1] + bg_rgb[2]) / 3 < 128
    
    # Font pairs
    font_configs = {
        'Modern': {
            'import': 'https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap',
            'heading': "'Syne', sans-serif",
            'body': "'DM Sans', sans-serif"
        },
        'Editorial': {
            'import': 'https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Lato:wght@300;400;700&display=swap',
            'heading': "'Playfair Display', serif",
            'body': "'Lato', sans-serif"
        },
        'Technical': {
            'import': 'https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap',
            'heading': "'IBM Plex Mono', monospace",
            'body': "'IBM Plex Sans', sans-serif"
        },
        'Elegant': {
            'import': 'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;1,400&family=Josefin+Sans:wght@300;400;600&display=swap',
            'heading': "'Cormorant Garamond', serif",
            'body': "'Josefin Sans', sans-serif"
        },
        'Bold': {
            'import': 'https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500&display=swap',
            'heading': "'Bebas Neue', display",
            'body': "'Inter', sans-serif"
        },
        'Futuristic': {
            'import': 'https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap',
            'heading': "'Orbitron', sans-serif",
            'body': "'Rajdhani', sans-serif"
        }
    }
    
    fonts = font_configs.get(font_pair, font_configs['Modern'])
    
    # Animation CSS
    animation_css = ""
    if animation_style == 'Smooth':
        animation_css = """
        @keyframes fadeUp { from { opacity:0; transform:translateY(30px); } to { opacity:1; transform:translateY(0); } }
        @keyframes fadeIn { from { opacity:0; } to { opacity:1; } }
        @keyframes slideRight { from { opacity:0; transform:translateX(-20px); } to { opacity:1; transform:translateX(0); } }
        .anim-fade-up { animation: fadeUp 0.7s ease forwards; }
        .anim-fade { animation: fadeIn 0.6s ease forwards; }
        .anim-slide { animation: slideRight 0.6s ease forwards; }
        .anim-delay-1 { animation-delay: 0.1s; opacity: 0; }
        .anim-delay-2 { animation-delay: 0.2s; opacity: 0; }
        .anim-delay-3 { animation-delay: 0.3s; opacity: 0; }
        .anim-delay-4 { animation-delay: 0.4s; opacity: 0; }
        .anim-delay-5 { animation-delay: 0.5s; opacity: 0; }
        .anim-delay-6 { animation-delay: 0.6s; opacity: 0; }
        """
        hero_classes = "anim-fade-up"
        subtitle_classes = "anim-fade-up anim-delay-1"
        body_classes = "anim-fade-up anim-delay-2"
        cta_classes = "anim-fade-up anim-delay-3"
    elif animation_style == 'Dramatic':
        animation_css = """
        @keyframes zoomIn { from { opacity:0; transform:scale(0.85); } to { opacity:1; transform:scale(1); } }
        @keyframes slideUp { from { opacity:0; transform:translateY(60px); } to { opacity:1; transform:translateY(0); } }
        .anim-fade-up { animation: zoomIn 0.9s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        .anim-fade { animation: zoomIn 0.7s ease forwards; }
        .anim-slide { animation: slideUp 0.8s ease forwards; }
        .anim-delay-1 { animation-delay: 0.15s; opacity: 0; }
        .anim-delay-2 { animation-delay: 0.3s; opacity: 0; }
        .anim-delay-3 { animation-delay: 0.45s; opacity: 0; }
        .anim-delay-4 { animation-delay: 0.6s; opacity: 0; }
        .anim-delay-5 { animation-delay: 0.75s; opacity: 0; }
        .anim-delay-6 { animation-delay: 0.9s; opacity: 0; }
        """
        hero_classes = "anim-fade-up"
        subtitle_classes = "anim-fade-up anim-delay-1"
        body_classes = "anim-fade-up anim-delay-2"
        cta_classes = "anim-fade-up anim-delay-3"
    else:
        animation_css = ""
        hero_classes = subtitle_classes = body_classes = cta_classes = ""

    # Background effects
    bg_effect = ""
    if s.get('bg_effect') == 'Gradient Mesh':
        bg_effect = f"""
        background: 
            radial-gradient(ellipse at 0% 0%, rgba({brand_rgb[0]},{brand_rgb[1]},{brand_rgb[2]},0.15) 0%, transparent 60%),
            radial-gradient(ellipse at 100% 100%, rgba({accent_rgb[0]},{accent_rgb[1]},{accent_rgb[2]},0.12) 0%, transparent 60%),
            {bg_color};
        """
    elif s.get('bg_effect') == 'Dots':
        bg_effect = f"""
        background-color: {bg_color};
        background-image: radial-gradient(circle, rgba({brand_rgb[0]},{brand_rgb[1]},{brand_rgb[2]},0.12) 1px, transparent 1px);
        background-size: 28px 28px;
        """
    elif s.get('bg_effect') == 'Lines':
        bg_effect = f"""
        background-color: {bg_color};
        background-image: repeating-linear-gradient(0deg, rgba({brand_rgb[0]},{brand_rgb[1]},{brand_rgb[2]},0.05) 0px, rgba({brand_rgb[0]},{brand_rgb[1]},{brand_rgb[2]},0.05) 1px, transparent 1px, transparent 40px);
        """
    elif s.get('bg_effect') == 'Noise':
        bg_effect = f"background-color: {bg_color};"
    else:
        bg_effect = f"background-color: {bg_color};"
    
    # NAV
    nav_position = "position: sticky; top: 0; z-index: 1000;" if nav_sticky else ""
    nav_html = ""
    if show_nav:
        nav_links_html = " ".join([f'<a href="#{l.lower()}">{l}</a>' for l in data.get('nav_links', ['Features', 'About', 'Contact'])])
        nav_html = f"""
    <nav class="nav" style="{nav_position}">
        <div class="nav-inner">
            <div class="nav-brand">{data.get('brand_name', 'Brand')}</div>
            <div class="nav-links">{nav_links_html}</div>
            <a href="{cta_url}" class="nav-cta">{data.get('cta_primary', 'Get Started')}</a>
            <button class="nav-hamburger" onclick="document.querySelector('.nav-links').classList.toggle('open')">☰</button>
        </div>
    </nav>"""

    # HERO section based on layout
    if hero_layout == 'Centered':
        hero_html = f"""
    <section class="hero hero-centered">
        <div class="hero-bg-shape"></div>
        <div class="container">
            <div class="hero-badge {hero_classes}">{data.get('social_proof', '10,000+ users')}</div>
            <h1 class="{subtitle_classes}">{data.get('headline', 'Your Headline Here')}</h1>
            <p class="hero-sub {body_classes}">{data.get('subheadline', 'Your subheadline here.')}</p>
            <p class="hero-body {body_classes}">{data.get('hero_body', '')}</p>
            <div class="hero-actions {cta_classes}">
                <a href="{cta_url}" class="btn btn-primary">{data.get('cta_primary', 'Get Started')}</a>
                <a href="#features" class="btn btn-ghost">{data.get('cta_secondary', 'Learn More')} →</a>
            </div>
            <div class="hero-email-form {cta_classes}">
                <input type="email" placeholder="{data.get('email_placeholder', 'your@email.com')}" class="email-input">
                <button class="btn btn-primary">{data.get('cta_primary', 'Start Free')}</button>
            </div>
        </div>
    </section>"""
    elif hero_layout == 'Split':
        hero_html = f"""
    <section class="hero hero-split">
        <div class="container hero-split-inner">
            <div class="hero-split-content">
                <div class="hero-badge {hero_classes}">{data.get('social_proof', '10,000+ users')}</div>
                <h1 class="{subtitle_classes}">{data.get('headline', 'Your Headline Here')}</h1>
                <p class="hero-sub {body_classes}">{data.get('subheadline', 'Your subheadline here.')}</p>
                <p class="hero-body {body_classes}">{data.get('hero_body', '')}</p>
                <div class="hero-actions {cta_classes}">
                    <a href="{cta_url}" class="btn btn-primary">{data.get('cta_primary', 'Get Started')}</a>
                    <a href="#features" class="btn btn-ghost">{data.get('cta_secondary', 'Learn More')} →</a>
                </div>
            </div>
            <div class="hero-split-visual">
                <div class="hero-mockup">
                    <div class="mockup-bar">
                        <span></span><span></span><span></span>
                    </div>
                    <div class="mockup-content">
                        <div class="mockup-line wide"></div>
                        <div class="mockup-line medium"></div>
                        <div class="mockup-line short"></div>
                        <div class="mockup-card"></div>
                        <div class="mockup-row">
                            <div class="mockup-card small"></div>
                            <div class="mockup-card small"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>"""
    else:  # Minimal
        hero_html = f"""
    <section class="hero hero-minimal">
        <div class="container">
            <p class="hero-eyebrow {hero_classes}">{data.get('tagline', 'Tagline here')}</p>
            <h1 class="{subtitle_classes}">{data.get('headline', 'Your Headline Here')}</h1>
            <div class="hero-divider"></div>
            <p class="hero-sub {body_classes}">{data.get('subheadline', 'Your subheadline here.')}</p>
            <div class="hero-actions {cta_classes}">
                <a href="{cta_url}" class="btn btn-primary">{data.get('cta_primary', 'Get Started')}</a>
                <a href="#features" class="btn btn-ghost">{data.get('cta_secondary', 'Learn More')} →</a>
            </div>
        </div>
    </section>"""

    # STATS SECTION
    stats_html = ""
    if show_stats and data.get('stats'):
        stats_items = " ".join([f'<div class="stat-item"><div class="stat-num">{s["num"]}</div><div class="stat-label">{s["label"]}</div></div>' for s in data['stats']])
        stats_html = f"""
    <section class="stats-section">
        <div class="container">
            <div class="stats-grid">{stats_items}</div>
        </div>
    </section>"""

    # FEATURES SECTION
    features_html = ""
    if data.get('features'):
        feats = data['features']
        feature_cards = ""
        for i, f in enumerate(feats):
            delay_class = f"anim-delay-{min(i+1, 6)}" if animation_style != 'None' else ""
            feature_cards += f"""
            <div class="feature-card anim-fade-up {delay_class}" id="feature-{i}">
                <div class="feature-icon">{f.get('icon', '⚡')}</div>
                <h3 class="feature-title">{f.get('title', 'Feature')}</h3>
                <p class="feature-desc">{f.get('desc', '')}</p>
            </div>"""
        
        features_html = f"""
    <section class="features-section" id="features">
        <div class="container">
            <div class="section-header">
                <span class="section-eyebrow">Why Choose Us</span>
                <h2>Everything you need to <em>succeed</em></h2>
            </div>
            <div class="features-grid">{feature_cards}
            </div>
        </div>
    </section>"""

    # TESTIMONIALS
    testimonials_html = ""
    if show_testimonials and data.get('testimonials'):
        testimonial_cards = ""
        for t in data['testimonials']:
            stars = "★" * t.get('rating', 5)
            testimonial_cards += f"""
            <div class="testimonial-card">
                <div class="stars">{stars}</div>
                <p class="testimonial-text">"{t.get('text', '')}"</p>
                <div class="testimonial-author">
                    <div class="author-avatar">{t.get('name', 'A')[0]}</div>
                    <div>
                        <div class="author-name">{t.get('name', '')}</div>
                        <div class="author-role">{t.get('role', '')}</div>
                    </div>
                </div>
            </div>"""
        
        testimonials_html = f"""
    <section class="testimonials-section" id="testimonials">
        <div class="container">
            <div class="section-header">
                <span class="section-eyebrow">Social Proof</span>
                <h2>Loved by <em>thousands</em></h2>
            </div>
            <div class="testimonials-grid">{testimonial_cards}
            </div>
        </div>
    </section>"""

    # FAQ
    faq_html = ""
    if show_faq and data.get('faq'):
        faq_items = ""
        for i, item in enumerate(data['faq']):
            faq_items += f"""
            <div class="faq-item">
                <button class="faq-q" onclick="toggleFAQ(this)">
                    <span>{item.get('q', '')}</span>
                    <span class="faq-icon">+</span>
                </button>
                <div class="faq-a"><p>{item.get('a', '')}</p></div>
            </div>"""
        
        faq_html = f"""
    <section class="faq-section" id="faq">
        <div class="container">
            <div class="section-header">
                <span class="section-eyebrow">FAQ</span>
                <h2>Got <em>questions?</em></h2>
            </div>
            <div class="faq-list">{faq_items}
            </div>
        </div>
    </section>"""

    # CTA BANNER
    cta_banner_html = ""
    if show_cta_banner:
        cta_banner_html = f"""
    <section class="cta-banner">
        <div class="container">
            <div class="cta-banner-inner">
                <div>
                    <h2>{data.get('headline', 'Ready to get started?')}</h2>
                    <p>{data.get('footer_text', 'Join thousands of happy customers today.')}</p>
                </div>
                <div class="cta-banner-actions">
                    <a href="{cta_url}" class="btn btn-primary btn-lg">{data.get('cta_primary', 'Get Started')} →</a>
                    <a href="#features" class="btn btn-ghost">{data.get('cta_secondary', 'Learn More')}</a>
                </div>
            </div>
        </div>
    </section>"""

    # FOOTER
    footer_html = f"""
    <footer class="footer">
        <div class="container">
            <div class="footer-inner">
                <div class="footer-brand">
                    <div class="footer-logo">{data.get('brand_name', 'Brand')}</div>
                    <p class="footer-tagline">{data.get('tagline', '')}</p>
                </div>
                <div class="footer-copy">© {datetime.now().year} {data.get('brand_name', 'Brand')}. All rights reserved.</div>
            </div>
        </div>
    </footer>"""

    # FULL HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{data.get('subheadline', '')}">
    <title>{data.get('headline', 'Landing Page')} — {data.get('brand_name', 'Brand')}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="{fonts['import']}" rel="stylesheet">
    <style>
        /* ── RESET & BASE ── */
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        :root {{
            --brand: {brand_color};
            --accent: {accent_color};
            --bg: {bg_color};
            --text: {text_color};
            --brand-rgb: {brand_rgb[0]}, {brand_rgb[1]}, {brand_rgb[2]};
            --accent-rgb: {accent_rgb[0]}, {accent_rgb[1]}, {accent_rgb[2]};
            --surface: {'rgba(255,255,255,0.06)' if is_dark else 'rgba(0,0,0,0.04)'};
            --border: {'rgba(255,255,255,0.1)' if is_dark else 'rgba(0,0,0,0.1)'};
            --muted: {'rgba(255,255,255,0.5)' if is_dark else 'rgba(0,0,0,0.45)'};
            --heading-font: {fonts['heading']};
            --body-font: {fonts['body']};
        }}

        html {{ scroll-behavior: smooth; }}

        body {{
            font-family: var(--body-font);
            {bg_effect}
            color: var(--text);
            line-height: 1.65;
            font-size: 16px;
            -webkit-font-smoothing: antialiased;
        }}

        /* ── ANIMATIONS ── */
        {animation_css}

        /* ── CONTAINER ── */
        .container {{
            max-width: 1160px;
            margin: 0 auto;
            padding: 0 24px;
        }}

        /* ── NAV ── */
        .nav {{
            background: {'rgba(7,8,15,0.85)' if is_dark else 'rgba(255,255,255,0.85)'};
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border);
        }}
        .nav-inner {{
            max-width: 1160px;
            margin: 0 auto;
            padding: 0 24px;
            height: 68px;
            display: flex;
            align-items: center;
            gap: 2rem;
        }}
        .nav-brand {{
            font-family: var(--heading-font);
            font-size: 1.4rem;
            font-weight: 800;
            color: var(--brand);
            flex-shrink: 0;
            letter-spacing: 0.03em;
        }}
        .nav-links {{
            display: flex;
            gap: 1.5rem;
            flex: 1;
        }}
        .nav-links a {{
            color: var(--muted);
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
            transition: color 0.2s;
        }}
        .nav-links a:hover {{ color: var(--text); }}
        .nav-cta {{
            background: var(--brand);
            color: {'#fff' if not is_dark else '#000'};
            padding: 0.5rem 1.2rem;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.875rem;
            transition: all 0.2s;
            flex-shrink: 0;
        }}
        .nav-cta:hover {{ opacity: 0.9; transform: translateY(-1px); }}
        .nav-hamburger {{
            display: none;
            background: none;
            border: none;
            color: var(--text);
            font-size: 1.4rem;
            cursor: pointer;
        }}

        /* ── HERO ── */
        .hero {{
            padding: 100px 0 80px;
            position: relative;
            overflow: hidden;
        }}
        .hero-bg-shape {{
            position: absolute;
            top: -200px;
            left: 50%;
            transform: translateX(-50%);
            width: 800px;
            height: 800px;
            background: radial-gradient(circle, rgba(var(--brand-rgb), 0.12) 0%, transparent 65%);
            pointer-events: none;
        }}

        /* CENTERED HERO */
        .hero-centered .container {{
            text-align: center;
            max-width: 780px;
        }}
        .hero-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            background: rgba(var(--brand-rgb), 0.12);
            border: 1px solid rgba(var(--brand-rgb), 0.3);
            color: var(--brand);
            padding: 0.35rem 1rem;
            border-radius: 100px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            letter-spacing: 0.03em;
        }}
        .hero-centered h1 {{
            font-family: var(--heading-font);
            font-size: clamp(2.5rem, 6vw, 4.5rem);
            font-weight: 800;
            line-height: 1.1;
            letter-spacing: -0.02em;
            margin-bottom: 1.25rem;
            background: linear-gradient(135deg, var(--text) 0%, rgba(var(--brand-rgb), 0.9) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .hero-sub {{
            font-size: 1.2rem;
            color: var(--muted);
            margin-bottom: 1rem;
            font-weight: 400;
            line-height: 1.5;
        }}
        .hero-body {{
            font-size: 1rem;
            color: var(--muted);
            margin-bottom: 2rem;
            line-height: 1.7;
            max-width: 580px;
            margin-left: auto;
            margin-right: auto;
        }}
        .hero-actions {{
            display: flex;
            gap: 0.75rem;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 1.5rem;
        }}
        .hero-email-form {{
            display: flex;
            gap: 0.5rem;
            max-width: 440px;
            margin: 0 auto;
            padding: 0.4rem;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 10px;
        }}
        .email-input {{
            flex: 1;
            background: none;
            border: none;
            outline: none;
            color: var(--text);
            font-family: var(--body-font);
            font-size: 0.9rem;
            padding: 0.4rem 0.75rem;
        }}
        .email-input::placeholder {{ color: var(--muted); }}

        /* SPLIT HERO */
        .hero-split {{ padding: 80px 0 60px; }}
        .hero-split-inner {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4rem;
            align-items: center;
        }}
        .hero-split h1 {{
            font-family: var(--heading-font);
            font-size: clamp(2rem, 5vw, 3.5rem);
            font-weight: 800;
            line-height: 1.1;
            letter-spacing: -0.02em;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, var(--text) 0%, rgba(var(--brand-rgb), 0.9) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .hero-mockup {{
            background: {'rgba(255,255,255,0.04)' if is_dark else 'rgba(0,0,0,0.03)'};
            border: 1px solid var(--border);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 24px 60px rgba(0,0,0,0.3);
        }}
        .mockup-bar {{
            display: flex;
            gap: 6px;
            padding: 12px 16px;
            background: var(--surface);
            border-bottom: 1px solid var(--border);
        }}
        .mockup-bar span {{
            width: 10px; height: 10px;
            border-radius: 50%;
            background: var(--border);
        }}
        .mockup-bar span:nth-child(1) {{ background: #ff5f57; }}
        .mockup-bar span:nth-child(2) {{ background: #febc2e; }}
        .mockup-bar span:nth-child(3) {{ background: #28c840; }}
        .mockup-content {{ padding: 20px; display: flex; flex-direction: column; gap: 12px; }}
        .mockup-line {{ height: 10px; background: var(--border); border-radius: 4px; }}
        .mockup-line.wide {{ width: 100%; }}
        .mockup-line.medium {{ width: 70%; }}
        .mockup-line.short {{ width: 45%; }}
        .mockup-card {{
            height: 80px;
            background: linear-gradient(135deg, rgba(var(--brand-rgb),0.15), rgba(var(--accent-rgb),0.1));
            border: 1px solid rgba(var(--brand-rgb),0.2);
            border-radius: 8px;
        }}
        .mockup-card.small {{ height: 60px; flex: 1; }}
        .mockup-row {{ display: flex; gap: 12px; }}

        /* MINIMAL HERO */
        .hero-minimal {{ padding: 120px 0 80px; }}
        .hero-eyebrow {{
            font-size: 0.75rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: var(--brand);
            font-weight: 700;
            margin-bottom: 1rem;
            display: block;
        }}
        .hero-minimal h1 {{
            font-family: var(--heading-font);
            font-size: clamp(3rem, 8vw, 7rem);
            font-weight: 800;
            line-height: 1.0;
            letter-spacing: -0.03em;
            margin-bottom: 1.5rem;
        }}
        .hero-divider {{
            width: 60px;
            height: 3px;
            background: var(--brand);
            margin-bottom: 1.5rem;
        }}

        /* ── BUTTONS ── */
        .btn {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.75rem 1.75rem;
            border-radius: 8px;
            text-decoration: none;
            font-family: var(--body-font);
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.2s ease;
            cursor: pointer;
            border: 2px solid transparent;
            white-space: nowrap;
        }}
        .btn-primary {{
            background: var(--brand);
            color: {'#fff' if not is_dark else '#000'};
            box-shadow: 0 4px 14px rgba(var(--brand-rgb), 0.35);
        }}
        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(var(--brand-rgb), 0.45);
            opacity: 0.92;
        }}
        .btn-ghost {{
            border-color: var(--border);
            color: var(--text);
            background: var(--surface);
        }}
        .btn-ghost:hover {{
            border-color: var(--brand);
            color: var(--brand);
        }}
        .btn-lg {{
            padding: 1rem 2.25rem;
            font-size: 1rem;
        }}

        /* ── STATS ── */
        .stats-section {{
            padding: 60px 0;
            border-top: 1px solid var(--border);
            border-bottom: 1px solid var(--border);
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 2rem;
            text-align: center;
        }}
        .stat-item .stat-num {{
            font-family: var(--heading-font);
            font-size: 2.8rem;
            font-weight: 800;
            color: var(--brand);
            letter-spacing: 0.02em;
            line-height: 1;
            margin-bottom: 0.4rem;
        }}
        .stat-item .stat-label {{
            font-size: 0.8rem;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 600;
        }}

        /* ── SECTION HEADERS ── */
        .section-header {{
            text-align: center;
            margin-bottom: 4rem;
        }}
        .section-eyebrow {{
            display: inline-block;
            font-size: 0.75rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: var(--brand);
            font-weight: 700;
            margin-bottom: 0.75rem;
            padding: 0.25rem 0.75rem;
            background: rgba(var(--brand-rgb), 0.1);
            border-radius: 100px;
        }}
        .section-header h2 {{
            font-family: var(--heading-font);
            font-size: clamp(2rem, 4vw, 3rem);
            font-weight: 800;
            letter-spacing: -0.02em;
            line-height: 1.2;
        }}
        .section-header h2 em {{
            font-style: normal;
            color: var(--brand);
        }}

        /* ── FEATURES ── */
        .features-section {{
            padding: 100px 0;
        }}
        .features-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
        }}
        .feature-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 2rem;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        .feature-card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0;
            right: 0; height: 2px;
            background: linear-gradient(90deg, var(--brand), var(--accent));
            opacity: 0;
            transition: opacity 0.3s;
        }}
        .feature-card:hover {{
            transform: translateY(-4px);
            border-color: rgba(var(--brand-rgb), 0.35);
            box-shadow: 0 12px 32px rgba(var(--brand-rgb), 0.12);
        }}
        .feature-card:hover::before {{ opacity: 1; }}
        .feature-icon {{
            font-size: 2rem;
            margin-bottom: 1rem;
            display: block;
        }}
        .feature-title {{
            font-family: var(--heading-font);
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 0.6rem;
            color: var(--text);
        }}
        .feature-desc {{
            font-size: 0.9rem;
            color: var(--muted);
            line-height: 1.6;
        }}

        /* ── TESTIMONIALS ── */
        .testimonials-section {{
            padding: 100px 0;
            background: var(--surface);
        }}
        .testimonials-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
        }}
        .testimonial-card {{
            background: {'rgba(255,255,255,0.03)' if is_dark else 'rgba(255,255,255,0.8)'};
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.75rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}
        .stars {{ color: #fbbf24; font-size: 1rem; letter-spacing: 2px; }}
        .testimonial-text {{
            font-size: 0.95rem;
            line-height: 1.7;
            color: var(--text);
            flex: 1;
            font-style: italic;
        }}
        .testimonial-author {{ display: flex; align-items: center; gap: 0.75rem; }}
        .author-avatar {{
            width: 40px; height: 40px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--brand), var(--accent));
            display: flex; align-items: center; justify-content: center;
            font-weight: 700;
            font-size: 1rem;
            color: #fff;
            flex-shrink: 0;
        }}
        .author-name {{
            font-weight: 700;
            font-size: 0.9rem;
            color: var(--text);
        }}
        .author-role {{
            font-size: 0.78rem;
            color: var(--muted);
        }}

        /* ── FAQ ── */
        .faq-section {{
            padding: 100px 0;
        }}
        .faq-list {{
            max-width: 700px;
            margin: 0 auto;
        }}
        .faq-item {{
            border-bottom: 1px solid var(--border);
        }}
        .faq-q {{
            width: 100%;
            background: none;
            border: none;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.25rem 0;
            font-family: var(--body-font);
            font-weight: 600;
            font-size: 1rem;
            color: var(--text);
            text-align: left;
            gap: 1rem;
        }}
        .faq-icon {{
            font-size: 1.25rem;
            color: var(--brand);
            transition: transform 0.3s;
            flex-shrink: 0;
        }}
        .faq-q.open .faq-icon {{ transform: rotate(45deg); }}
        .faq-a {{
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.4s ease;
        }}
        .faq-a.open {{ max-height: 200px; }}
        .faq-a p {{
            padding-bottom: 1.25rem;
            color: var(--muted);
            font-size: 0.95rem;
            line-height: 1.7;
        }}

        /* ── CTA BANNER ── */
        .cta-banner {{
            padding: 80px 0;
            background: linear-gradient(135deg, rgba(var(--brand-rgb),0.12) 0%, rgba(var(--accent-rgb),0.08) 100%);
            border-top: 1px solid rgba(var(--brand-rgb),0.2);
            border-bottom: 1px solid rgba(var(--brand-rgb),0.2);
        }}
        .cta-banner-inner {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 2rem;
            flex-wrap: wrap;
        }}
        .cta-banner h2 {{
            font-family: var(--heading-font);
            font-size: clamp(1.5rem, 3vw, 2.5rem);
            font-weight: 800;
            letter-spacing: -0.01em;
            margin-bottom: 0.4rem;
        }}
        .cta-banner p {{
            color: var(--muted);
            font-size: 1rem;
        }}
        .cta-banner-actions {{
            display: flex;
            gap: 0.75rem;
            flex-shrink: 0;
            flex-wrap: wrap;
        }}

        /* ── FOOTER ── */
        .footer {{
            padding: 40px 0;
            border-top: 1px solid var(--border);
        }}
        .footer-inner {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            flex-wrap: wrap;
        }}
        .footer-logo {{
            font-family: var(--heading-font);
            font-size: 1.4rem;
            font-weight: 800;
            color: var(--brand);
            letter-spacing: 0.03em;
            margin-bottom: 0.25rem;
        }}
        .footer-tagline {{
            font-size: 0.8rem;
            color: var(--muted);
        }}
        .footer-copy {{
            font-size: 0.8rem;
            color: var(--muted);
        }}

        /* ── RESPONSIVE ── */
        @media (max-width: 900px) {{
            .hero-split-inner {{ grid-template-columns: 1fr; }}
            .hero-split-visual {{ display: none; }}
            .features-grid {{ grid-template-columns: 1fr 1fr; }}
            .testimonials-grid {{ grid-template-columns: 1fr; }}
            .stats-grid {{ grid-template-columns: 2fr 2fr; }}
        }}
        @media (max-width: 640px) {{
            .nav-links {{ display: none; }}
            .nav-links.open {{ display: flex; flex-direction: column; position: absolute; top: 68px; left: 0; right: 0; background: var(--bg); padding: 1rem; border-bottom: 1px solid var(--border); }}
            .nav-hamburger {{ display: block; }}
            .nav-inner {{ position: relative; }}
            .features-grid {{ grid-template-columns: 1fr; }}
            .stats-grid {{ grid-template-columns: 1fr 1fr; }}
            .cta-banner-inner {{ flex-direction: column; text-align: center; }}
            .hero-email-form {{ flex-direction: column; }}
        }}
    </style>
</head>
<body>
{nav_html}
{hero_html}
{stats_html}
{features_html}
{testimonials_html}
{faq_html}
{cta_banner_html}
{footer_html}

<script>
function toggleFAQ(btn) {{
    btn.classList.toggle('open');
    const answer = btn.nextElementSibling;
    answer.classList.toggle('open');
}}

// Intersection Observer for scroll animations
if ('IntersectionObserver' in window) {{
    const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                const el = entry.target;
                el.style.animationPlayState = 'running';
                observer.unobserve(el);
            }}
        }});
    }}, {{ threshold: 0.1 }});

    document.querySelectorAll('.anim-delay-1, .anim-delay-2, .anim-delay-3, .anim-delay-4, .anim-delay-5, .anim-delay-6').forEach(el => {{
        el.style.animationPlayState = 'paused';
        observer.observe(el);
    }});
}}
</script>
</body>
</html>"""
    
    return html

# ─────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────
defaults = {
    'page_data': None,
    'description': '',
    'brand_color': '#6c63ff',
    'accent_color': '#ff6584',
    'bg_color': '#0d0d18',
    'text_color': '#f0f0ff',
    'cta_url': '#signup',
    'font_pair': 'Modern',
    'layout_style': 'Standard',
    'hero_layout': 'Centered',
    'animation_style': 'Smooth',
    'bg_effect': 'Gradient Mesh',
    'nav_sticky': True,
    'show_testimonials': True,
    'show_faq': True,
    'show_stats': True,
    'show_cta_banner': True,
    'show_nav': True,
    'generated_html': None,
    'gen_count': 0,
    'tone': 'Professional',
    'industry': 'Technology',
    'audience': 'B2B professionals',
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div class="forge-header">
        <div class="forge-logo">PAGE<span>FORGE</span></div>
        <div class="forge-tagline">AI Landing Page Studio</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='padding: 1rem 1.25rem 0;'>", unsafe_allow_html=True)
    
    # API KEY
    st.markdown('<span class="section-label">🔑 OpenAI API Key</span>', unsafe_allow_html=True)
    api_key = st.text_input("API Key", type="password", placeholder="sk-...", label_visibility="collapsed")
    
    model = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"], label_visibility="visible")
    
    st.markdown('<hr class="forge-divider">', unsafe_allow_html=True)
    st.markdown('<span class="section-label">📊 Generation Stats</span>', unsafe_allow_html=True)
    
    gen_count = st.session_state.gen_count
    has_data = st.session_state.page_data is not None
    
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-box"><div class="stat-num">{gen_count}</div><div class="stat-label">Generated</div></div>
        <div class="stat-box"><div class="stat-num">{'✓' if has_data else '—'}</div><div class="stat-label">Page Ready</div></div>
        <div class="stat-box"><div class="stat-num">{len(st.session_state.page_data.get('features', [])) if has_data else '—'}</div><div class="stat-label">Sections</div></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<hr class="forge-divider">', unsafe_allow_html=True)
    st.markdown('<span class="section-label">📋 Quick Guide</span>', unsafe_allow_html=True)
    
    steps = [
        ("1", "Enter business description + settings"),
        ("2", "Generate AI content"),
        ("3", "Customize in editor tabs"),
        ("4", "Preview & export HTML"),
    ]
    for num, text in steps:
        st.markdown(f"""<div style="display:flex;gap:0.75rem;align-items:flex-start;margin-bottom:0.5rem;">
            <div class="step-num">{num}</div>
            <div style="font-size:0.8rem;color:#5a5f7a;padding-top:0.3rem;">{text}</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────
# MAIN AREA
# ─────────────────────────────────────────

st.markdown("""
<div class="main-title">PAGE<span class="accent">FORGE</span></div>
<p style="font-family:'Space Mono',monospace;font-size:0.72rem;color:#5a5f7a;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:1.5rem;">
AI Landing Page Studio — Generate · Customize · Export
</p>
""", unsafe_allow_html=True)

# ─── INPUT ROW ───
with st.expander("⚙️  Page Settings & Description", expanded=True):
    col_desc, col_meta = st.columns([2, 1])
    
    with col_desc:
        st.markdown('<span class="section-label">💡 Business Description</span>', unsafe_allow_html=True)
        description = st.text_area(
            "Description",
            value=st.session_state.description,
            height=120,
            placeholder="Describe your product, service, or business. Include your unique value proposition, target audience, and key benefits. Be specific for best results...",
            label_visibility="collapsed"
        )
        st.session_state.description = description
    
    with col_meta:
        tone = st.selectbox("Tone & Voice", 
            ["Professional", "Playful", "Bold & Edgy", "Minimalist", "Luxury", "Technical", "Friendly", "Urgent"],
            index=["Professional", "Playful", "Bold & Edgy", "Minimalist", "Luxury", "Technical", "Friendly", "Urgent"].index(st.session_state.tone)
        )
        st.session_state.tone = tone
        
        industry = st.selectbox("Industry",
            ["Technology", "SaaS", "E-commerce", "Healthcare", "Finance", "Education", "Creative", "Agency", "Real Estate", "Food & Beverage", "Other"],
            index=0
        )
        st.session_state.industry = industry
        
        audience = st.text_input("Target Audience", value=st.session_state.audience, placeholder="e.g. Marketing managers at B2B SaaS companies")
        st.session_state.audience = audience

# ─── GENERATE BUTTON ───
col_gen, col_tip = st.columns([1, 3])

with col_gen:
    gen_clicked = st.button("⚡ Generate Landing Page", use_container_width=True)

with col_tip:
    if not api_key:
        st.info("💡 Add your OpenAI API key in the sidebar to generate content")
    elif not description:
        st.info("💡 Enter a business description above, then click Generate")

if gen_clicked:
    if not api_key:
        st.error("❌ OpenAI API key required.")
    elif not description.strip():
        st.error("❌ Please enter a business description.")
    else:
        progress = st.progress(0)
        status = st.empty()
        
        status.markdown("🔄 Crafting your content with AI...")
        progress.progress(20)
        
        data = generate_all_content(description, tone, industry, audience, api_key, model)
        progress.progress(70)
        
        if data:
            st.session_state.page_data = data
            st.session_state.gen_count += 1
            
            status.markdown("🎨 Building preview...")
            progress.progress(90)
            time.sleep(0.3)
            progress.progress(100)
            status.success(f"✅ Landing page generated! {len(data.get('features', []))} features, {len(data.get('testimonials', []))} testimonials, {len(data.get('faq', []))} FAQs created.")
        else:
            progress.empty()
            status.error("❌ Generation failed. Check your API key and try again.")

st.markdown("---")

# ─────────────────────────────────────────
# MAIN EDITOR + PREVIEW (only when data exists)
# ─────────────────────────────────────────

if st.session_state.page_data:
    data = st.session_state.page_data
    
    # ─── EDITOR TABS ───
    tab_copy, tab_design, tab_sections, tab_code = st.tabs(["✏️ Copy Editor", "🎨 Design & Style", "🧩 Sections", "💻 Code"])
    
    with tab_copy:
        st.markdown('<div class="section-chip">COPY EDITOR</div>', unsafe_allow_html=True)
        
        # Hero content
        col_h, col_s = st.columns(2)
        with col_h:
            data['headline'] = st.text_input("🔥 Main Headline", value=data.get('headline', ''))
            data['subheadline'] = st.text_input("📌 Subheadline", value=data.get('subheadline', ''))
            data['brand_name'] = st.text_input("🏷️ Brand Name", value=data.get('brand_name', ''))
            data['tagline'] = st.text_input("✨ Tagline", value=data.get('tagline', ''))
        
        with col_s:
            data['cta_primary'] = st.text_input("🔘 Primary CTA Button", value=data.get('cta_primary', 'Get Started'))
            data['cta_secondary'] = st.text_input("🔲 Secondary CTA Button", value=data.get('cta_secondary', 'Learn More'))
            st.session_state.cta_url = st.text_input("🔗 CTA URL", value=st.session_state.cta_url)
            data['email_placeholder'] = st.text_input("📧 Email Placeholder", value=data.get('email_placeholder', 'your@email.com'))
        
        data['hero_body'] = st.text_area("📝 Hero Body Text", value=data.get('hero_body', ''), height=100)
        data['social_proof'] = st.text_input("🏆 Social Proof Badge", value=data.get('social_proof', ''))
        data['footer_text'] = st.text_input("👇 Footer Tagline", value=data.get('footer_text', ''))
        
        st.markdown("---")
        st.markdown('<span class="section-label">✨ Features</span>', unsafe_allow_html=True)
        
        features = data.get('features', [])
        cols_feat = st.columns(2)
        new_features = []
        for i, feat in enumerate(features):
            col = cols_feat[i % 2]
            with col:
                with st.expander(f"{feat.get('icon','⚡')} {feat.get('title', f'Feature {i+1}')}", expanded=False):
                    icon = st.text_input("Icon", value=feat.get('icon', '⚡'), key=f"ficon_{i}")
                    title = st.text_input("Title", value=feat.get('title', ''), key=f"ftitle_{i}")
                    desc = st.text_area("Description", value=feat.get('desc', ''), key=f"fdesc_{i}", height=80)
                    new_features.append({"icon": icon, "title": title, "desc": desc})
        data['features'] = new_features
        
        if st.button("➕ Add Feature"):
            data['features'].append({"icon": "⭐", "title": "New Feature", "desc": "Describe this feature's benefit"})
            st.rerun()
        
        st.markdown("---")
        st.markdown('<span class="section-label">💬 Testimonials</span>', unsafe_allow_html=True)
        
        testimonials = data.get('testimonials', [])
        for i, t in enumerate(testimonials):
            with st.expander(f"💬 {t.get('name', f'Testimonial {i+1}')}", expanded=False):
                col_t1, col_t2 = st.columns(2)
                with col_t1:
                    t['name'] = st.text_input("Name", value=t.get('name', ''), key=f"tname_{i}")
                    t['role'] = st.text_input("Role / Company", value=t.get('role', ''), key=f"trole_{i}")
                with col_t2:
                    t['rating'] = st.slider("Rating", 1, 5, t.get('rating', 5), key=f"trating_{i}")
                t['text'] = st.text_area("Testimonial Text", value=t.get('text', ''), key=f"ttext_{i}", height=80)
        
        st.markdown("---")
        st.markdown('<span class="section-label">❓ FAQ</span>', unsafe_allow_html=True)
        
        faq = data.get('faq', [])
        for i, item in enumerate(faq):
            with st.expander(f"❓ {item.get('q', f'FAQ {i+1}')[:50]}...", expanded=False):
                item['q'] = st.text_input("Question", value=item.get('q', ''), key=f"fq_{i}")
                item['a'] = st.text_area("Answer", value=item.get('a', ''), key=f"fa_{i}", height=80)
        
        st.markdown("---")
        st.markdown('<span class="section-label">📊 Stats</span>', unsafe_allow_html=True)
        
        stats = data.get('stats', [])
        stat_cols = st.columns(4)
        for i, stat in enumerate(stats):
            with stat_cols[i % 4]:
                stat['num'] = st.text_input("Number", value=stat.get('num', ''), key=f"snum_{i}")
                stat['label'] = st.text_input("Label", value=stat.get('label', ''), key=f"slabel_{i}")
    
    with tab_design:
        st.markdown('<div class="section-chip blue">DESIGN SYSTEM</div>', unsafe_allow_html=True)
        
        col_d1, col_d2 = st.columns(2)
        
        with col_d1:
            st.markdown("**Colors**")
            st.session_state.brand_color = st.color_picker("Brand Color", st.session_state.brand_color)
            st.session_state.accent_color = st.color_picker("Accent Color", st.session_state.accent_color)
            st.session_state.bg_color = st.color_picker("Background Color", st.session_state.bg_color)
            st.session_state.text_color = st.color_picker("Text Color", st.session_state.text_color)
            
            # Quick themes
            st.markdown("**Quick Color Themes**")
            theme_cols = st.columns(4)
            themes = {
                "Dark": ("#6c63ff", "#ff6584", "#0d0d18", "#f0f0ff"),
                "Light": ("#5c4ee5", "#ff4d8d", "#fafafa", "#1a1a2e"),
                "Forest": ("#2d8a5e", "#ff7043", "#0f1f17", "#e8f5e9"),
                "Gold": ("#c9a96e", "#ff6b6b", "#0f1117", "#f0ede8"),
                "Ocean": ("#0891b2", "#f59e0b", "#0c1523", "#e0f2fe"),
                "Fire": ("#ef4444", "#f97316", "#1c0a00", "#fef3e2"),
                "Purple": ("#9333ea", "#ec4899", "#0f0a1a", "#fdf4ff"),
                "Mono": ("#f5f5f5", "#888888", "#111111", "#f5f5f5"),
            }
            
            for i, (name, colors) in enumerate(themes.items()):
                col = theme_cols[i % 4]
                with col:
                    if st.button(name, key=f"theme_{name}"):
                        st.session_state.brand_color = colors[0]
                        st.session_state.accent_color = colors[1]
                        st.session_state.bg_color = colors[2]
                        st.session_state.text_color = colors[3]
                        st.rerun()
        
        with col_d2:
            st.markdown("**Typography**")
            st.session_state.font_pair = st.radio("Font Style", 
                ["Modern", "Editorial", "Technical", "Elegant", "Bold", "Futuristic"],
                index=["Modern", "Editorial", "Technical", "Elegant", "Bold", "Futuristic"].index(st.session_state.font_pair)
            )
            
            st.markdown("**Layout**")
            st.session_state.hero_layout = st.radio("Hero Layout",
                ["Centered", "Split", "Minimal"],
                index=["Centered", "Split", "Minimal"].index(st.session_state.hero_layout)
            )
            
            st.markdown("**Animation**")
            st.session_state.animation_style = st.radio("Animation Style",
                ["Smooth", "Dramatic", "None"],
                index=["Smooth", "Dramatic", "None"].index(st.session_state.animation_style)
            )
            
            st.markdown("**Background Effect**")
            st.session_state.bg_effect = st.radio("Background",
                ["Gradient Mesh", "Dots", "Lines", "Solid"],
                index=["Gradient Mesh", "Dots", "Lines", "Solid"].index(st.session_state.bg_effect)
            )
    
    with tab_sections:
        st.markdown('<div class="section-chip gold">SECTION CONTROL</div>', unsafe_allow_html=True)
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.session_state.show_nav = st.checkbox("🧭 Navigation Bar", value=st.session_state.show_nav)
            st.session_state.nav_sticky = st.checkbox("📌 Sticky Nav", value=st.session_state.nav_sticky)
            st.session_state.show_stats = st.checkbox("📊 Stats Section", value=st.session_state.show_stats)
            st.session_state.show_testimonials = st.checkbox("💬 Testimonials", value=st.session_state.show_testimonials)
        
        with col_s2:
            st.session_state.show_faq = st.checkbox("❓ FAQ Section", value=st.session_state.show_faq)
            st.session_state.show_cta_banner = st.checkbox("🎯 CTA Banner", value=st.session_state.show_cta_banner)
        
        st.markdown("---")
        st.markdown('<span class="section-label">🔗 Nav Links</span>', unsafe_allow_html=True)
        
        nav_links = data.get('nav_links', ['Features', 'Testimonials', 'Pricing', 'FAQ'])
        nav_links_str = ", ".join(nav_links)
        nav_edit = st.text_input("Nav Links (comma-separated)", value=nav_links_str)
        data['nav_links'] = [l.strip() for l in nav_edit.split(',') if l.strip()]
    
    with tab_code:
        st.markdown('<div class="section-chip success">CODE OUTPUT</div>', unsafe_allow_html=True)
        
        # Generate HTML
        settings = {
            'brand_color': st.session_state.brand_color,
            'accent_color': st.session_state.accent_color,
            'bg_color': st.session_state.bg_color,
            'text_color': st.session_state.text_color,
            'font_pair': st.session_state.font_pair,
            'hero_layout': st.session_state.hero_layout,
            'animation_style': st.session_state.animation_style,
            'bg_effect': st.session_state.bg_effect,
            'nav_sticky': st.session_state.nav_sticky,
            'show_nav': st.session_state.show_nav,
            'show_testimonials': st.session_state.show_testimonials,
            'show_faq': st.session_state.show_faq,
            'show_stats': st.session_state.show_stats,
            'show_cta_banner': st.session_state.show_cta_banner,
            'cta_url': st.session_state.cta_url,
        }
        
        html_output = generate_complete_html(data, settings)
        st.session_state.generated_html = html_output
        
        line_count = len(html_output.split('\n'))
        char_count = len(html_output)
        st.markdown(f"""
        <div class="tip-block">
        📄 <strong>{line_count} lines</strong> · {char_count:,} characters · Production-ready HTML with embedded CSS & JS
        </div>
        """, unsafe_allow_html=True)
        
        st.code(html_output[:3000] + f"\n\n... ({line_count - 80} more lines) ...", language="html")
    
    # ─────────────────────────────────────────
    # LIVE PREVIEW
    # ─────────────────────────────────────────
    
    st.markdown("---")
    st.markdown('<div class="section-chip">👁️ LIVE PREVIEW</div>', unsafe_allow_html=True)
    
    settings = {
        'brand_color': st.session_state.brand_color,
        'accent_color': st.session_state.accent_color,
        'bg_color': st.session_state.bg_color,
        'text_color': st.session_state.text_color,
        'font_pair': st.session_state.font_pair,
        'hero_layout': st.session_state.hero_layout,
        'animation_style': st.session_state.animation_style,
        'bg_effect': st.session_state.bg_effect,
        'nav_sticky': False,  # Disable sticky in preview
        'show_nav': st.session_state.show_nav,
        'show_testimonials': st.session_state.show_testimonials,
        'show_faq': st.session_state.show_faq,
        'show_stats': st.session_state.show_stats,
        'show_cta_banner': st.session_state.show_cta_banner,
        'cta_url': st.session_state.cta_url,
    }
    
    preview_html = generate_complete_html(data, settings)
    
    # Browser chrome mockup
    st.markdown("""
    <div class="preview-toolbar">
        <div class="preview-dot" style="background:#ff5f57"></div>
        <div class="preview-dot" style="background:#febc2e"></div>
        <div class="preview-dot" style="background:#28c840"></div>
        <div class="preview-url">yourlandingpage.com</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.components.v1.html(preview_html, height=900, scrolling=True)
    
    # ─────────────────────────────────────────
    # EXPORT SECTION
    # ─────────────────────────────────────────
    
    st.markdown("---")
    st.markdown('<div class="section-chip success">📦 EXPORT</div>', unsafe_allow_html=True)
    
    final_html = generate_complete_html(data, {**settings, 'nav_sticky': st.session_state.nav_sticky})
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    
    col_e1, col_e2, col_e3, col_e4 = st.columns(4)
    
    with col_e1:
        st.markdown("""<div class="export-card">
            <div class="export-card-title">📄 Full HTML</div>
            <div class="export-card-desc">Complete standalone HTML file with embedded CSS, fonts, and JavaScript. Upload anywhere.</div>
        </div>""", unsafe_allow_html=True)
        st.download_button(
            "⬇️ Download HTML",
            data=final_html,
            file_name=f"landing-page-{timestamp}.html",
            mime="text/html",
            use_container_width=True
        )
    
    with col_e2:
        json_str = json.dumps(data, indent=2)
        st.markdown("""<div class="export-card">
            <div class="export-card-title">🗃️ Content JSON</div>
            <div class="export-card-desc">All page content as structured JSON. Use to regenerate or import into other tools.</div>
        </div>""", unsafe_allow_html=True)
        st.download_button(
            "⬇️ Download JSON",
            data=json_str,
            file_name=f"page-content-{timestamp}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col_e3:
        settings_export = json.dumps({
            'brand_color': st.session_state.brand_color,
            'accent_color': st.session_state.accent_color,
            'bg_color': st.session_state.bg_color,
            'text_color': st.session_state.text_color,
            'font_pair': st.session_state.font_pair,
            'hero_layout': st.session_state.hero_layout,
            'animation_style': st.session_state.animation_style,
            'bg_effect': st.session_state.bg_effect,
        }, indent=2)
        st.markdown("""<div class="export-card">
            <div class="export-card-title">🎨 Design Settings</div>
            <div class="export-card-desc">Your color palette, fonts, and layout config as JSON for reuse.</div>
        </div>""", unsafe_allow_html=True)
        st.download_button(
            "⬇️ Design Config",
            data=settings_export,
            file_name=f"design-config-{timestamp}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col_e4:
        st.markdown("""<div class="export-card">
            <div class="export-card-title">🔄 Regenerate</div>
            <div class="export-card-desc">Not happy with the AI content? Regenerate specific sections or everything.</div>
        </div>""", unsafe_allow_html=True)
        if st.button("🔄 Regen Everything", use_container_width=True):
            if api_key and st.session_state.description:
                with st.spinner("Regenerating..."):
                    new_data = generate_all_content(
                        st.session_state.description, 
                        st.session_state.tone,
                        st.session_state.industry,
                        st.session_state.audience,
                        api_key, model
                    )
                    if new_data:
                        st.session_state.page_data = new_data
                        st.session_state.gen_count += 1
                        st.rerun()

else:
    # Empty state
    st.markdown("""
    <div style="text-align:center;padding:5rem 2rem;">
        <div style="font-size:4rem;margin-bottom:1rem;">⚡</div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;letter-spacing:0.08em;color:#e8eaf0;margin-bottom:0.5rem;">
            READY TO FORGE YOUR PAGE
        </div>
        <p style="font-family:'Space Mono',monospace;font-size:0.75rem;color:#5a5f7a;letter-spacing:0.1em;text-transform:uppercase;max-width:500px;margin:0 auto;">
            Enter your business description above, configure your settings, add your OpenAI API key and hit Generate.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="text-align:center;padding:1rem 0;">
    <span style="font-family:'Space Mono',monospace;font-size:0.65rem;color:#2e3245;letter-spacing:0.15em;text-transform:uppercase;">
        PAGEFORGE — AI LANDING PAGE STUDIO — BUILT WITH STREAMLIT & OPENAI
    </span>
</div>
""", unsafe_allow_html=True)
