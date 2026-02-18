import streamlit as st
import json
import re
import time
import hashlib
import random
from datetime import datetime
import base64

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="PageForge v2 — AI Landing Page Studio",
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
    --surface3: #1a1d2e;
    --border: #1e2133;
    --border2: #252840;
    --accent: #ff3c5f;
    --accent2: #ff7a4d;
    --blue: #4d7cff;
    --teal: #36d3c0;
    --gold: #ffc44d;
    --text: #e8eaf0;
    --muted: #5a5f7a;
    --muted2: #3d4060;
    --success: #36d37e;
    --warning: #ffb84d;
}

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}
.stApp { background: var(--bg) !important; }
#MainMenu, footer, header { visibility: hidden; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
    width: 300px !important;
}
section[data-testid="stSidebar"] > div { padding: 0 !important; }

/* ── INPUTS ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div,
.stNumberInput > div > div > input {
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
    box-shadow: 0 0 0 2px rgba(255,60,95,0.15) !important;
}
label, .stTextInput label, .stTextArea label, .stSelectbox label {
    color: var(--muted) !important;
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-family: 'Space Mono', monospace !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    padding: 0.6rem 1.25rem !important;
    border: none !important;
    border-radius: 6px !important;
    transition: all 0.15s ease !important;
    width: 100%;
}
.stButton > button:hover {
    background: #ff5571 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(255,60,95,0.4) !important;
}
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

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 4px !important;
    gap: 2px !important;
    flex-wrap: wrap !important;
}
.stTabs [data-baseweb="tab"] {
    color: var(--muted) !important;
    border-radius: 6px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.68rem !important;
    padding: 0.45rem 0.8rem !important;
}
.stTabs [aria-selected="true"] {
    background: var(--accent) !important;
    color: #fff !important;
    font-weight: 700 !important;
}

/* ── MISC ── */
.stSelectbox [data-baseweb="select"] > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
}
.stSuccess > div {
    background: rgba(54,211,126,0.1) !important;
    border: 1px solid rgba(54,211,126,0.3) !important;
    border-radius: 8px !important; color: var(--success) !important;
}
.stError > div {
    background: rgba(255,60,95,0.1) !important;
    border: 1px solid rgba(255,60,95,0.3) !important;
    border-radius: 8px !important; color: #ff6b85 !important;
}
.stInfo > div {
    background: rgba(77,124,255,0.1) !important;
    border: 1px solid rgba(77,124,255,0.3) !important;
    border-radius: 8px !important; color: #7a9fff !important;
}
.stWarning > div {
    background: rgba(255,184,77,0.1) !important;
    border: 1px solid rgba(255,184,77,0.3) !important;
    border-radius: 8px !important; color: var(--warning) !important;
}
.stCheckbox > label > div[data-testid="stCheckboxRoot"] {
    background: var(--surface2) !important;
    border-color: var(--border2) !important;
}
.stRadio > div { gap: 0.4rem !important; }
.stSlider > div > div > div { color: var(--text) !important; }
.stProgress > div > div { background: var(--accent) !important; }
.streamlit-expanderHeader {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
}

/* ── CUSTOM COMPONENTS ── */
.forge-header {
    padding: 1.5rem 1.25rem 1rem;
    border-bottom: 1px solid var(--border);
    background: linear-gradient(180deg, rgba(255,60,95,0.05) 0%, transparent 100%);
}
.forge-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    letter-spacing: 0.08em;
    color: var(--text);
    line-height: 1;
    margin-bottom: 0.2rem;
}
.forge-logo span { color: var(--accent); }
.forge-version {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: var(--muted);
    letter-spacing: 0.15em;
    text-transform: uppercase;
}
.section-chip {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: rgba(255,60,95,0.1); border: 1px solid rgba(255,60,95,0.25);
    border-radius: 4px; padding: 0.2rem 0.6rem;
    font-family: 'Space Mono', monospace; font-size: 0.62rem;
    letter-spacing: 0.12em; text-transform: uppercase; color: var(--accent);
    margin-bottom: 1rem;
}
.section-chip.blue { background: rgba(77,124,255,0.1); border-color: rgba(77,124,255,0.25); color: var(--blue); }
.section-chip.gold { background: rgba(255,196,77,0.1); border-color: rgba(255,196,77,0.25); color: var(--gold); }
.section-chip.teal { background: rgba(54,211,192,0.1); border-color: rgba(54,211,192,0.25); color: var(--teal); }
.section-chip.success { background: rgba(54,211,126,0.1); border-color: rgba(54,211,126,0.25); color: var(--success); }
.section-chip.purple { background: rgba(150,100,255,0.1); border-color: rgba(150,100,255,0.25); color: #9664ff; }

.section-label {
    font-family: 'Space Mono', monospace; font-size: 0.62rem;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: var(--muted); margin-bottom: 0.6rem; display: block;
}
.main-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem; letter-spacing: 0.06em;
    color: var(--text); line-height: 1; margin-bottom: 0.2rem;
}
.main-title .accent { color: var(--accent); }
.stat-row { display: flex; gap: 0.6rem; margin: 0.75rem 0; }
.stat-box {
    flex: 1; background: var(--surface2);
    border: 1px solid var(--border); border-radius: 6px;
    padding: 0.65rem; text-align: center;
}
.stat-num { font-family: 'Bebas Neue', sans-serif; font-size: 1.4rem; color: var(--accent); line-height: 1; }
.stat-label { font-family: 'Space Mono', monospace; font-size: 0.55rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.1em; margin-top: 0.2rem; }
.info-block {
    background: rgba(77,124,255,0.06); border-left: 3px solid var(--blue);
    border-radius: 0 6px 6px 0; padding: 0.65rem 0.9rem;
    margin: 0.6rem 0; font-size: 0.78rem; color: #8aacff; line-height: 1.6;
}
.tip-block {
    background: rgba(54,211,192,0.06); border-left: 3px solid var(--teal);
    border-radius: 0 6px 6px 0; padding: 0.65rem 0.9rem;
    margin: 0.6rem 0; font-size: 0.78rem; color: #6ee8dc; line-height: 1.6;
}
.warn-block {
    background: rgba(255,184,77,0.06); border-left: 3px solid var(--warning);
    border-radius: 0 6px 6px 0; padding: 0.65rem 0.9rem;
    margin: 0.6rem 0; font-size: 0.78rem; color: #ffc97a; line-height: 1.6;
}
.export-card {
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 8px; padding: 1rem;
    display: flex; flex-direction: column; gap: 0.4rem; height: 100%;
}
.export-card-title { font-family: 'Bebas Neue', sans-serif; font-size: 1rem; letter-spacing: 0.08em; color: var(--text); }
.export-card-desc { font-size: 0.73rem; color: var(--muted); line-height: 1.5; }
.preview-toolbar {
    display: flex; align-items: center; gap: 8px;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px 8px 0 0; padding: 0.5rem 0.75rem; border-bottom: none;
}
.preview-dot { width: 10px; height: 10px; border-radius: 50%; }
.preview-url {
    flex: 1; background: var(--surface2); border: 1px solid var(--border);
    border-radius: 4px; padding: 0.2rem 0.6rem;
    font-family: 'Space Mono', monospace; font-size: 0.62rem; color: var(--muted);
    margin-left: 0.5rem;
}
.score-bar-wrap { background: var(--surface3); border-radius: 4px; height: 6px; overflow: hidden; margin-top: 3px; }
.score-bar { height: 100%; border-radius: 4px; transition: width 0.4s ease; }
.score-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem; }
.score-label { font-family: 'Space Mono', monospace; font-size: 0.62rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; }
.score-val { font-family: 'Bebas Neue', sans-serif; font-size: 1rem; color: var(--text); letter-spacing: 0.05em; }
.template-card {
    background: var(--surface2); border: 2px solid var(--border);
    border-radius: 8px; padding: 0.75rem; cursor: pointer;
    transition: all 0.15s ease; text-align: center; margin-bottom: 0.5rem;
}
.template-card:hover { border-color: var(--accent); }
.template-card.active { border-color: var(--accent); background: rgba(255,60,95,0.08); }
.template-preview { width: 100%; height: 60px; border-radius: 4px; margin-bottom: 0.5rem; }
.changelog-item {
    display: flex; gap: 0.75rem; padding: 0.5rem 0;
    border-bottom: 1px solid var(--border2); font-size: 0.8rem;
}
.changelog-badge {
    background: rgba(255,60,95,0.15); color: var(--accent);
    border-radius: 4px; padding: 0.1rem 0.4rem;
    font-family: 'Space Mono', monospace; font-size: 0.6rem;
    font-weight: 700; white-space: nowrap; height: fit-content;
    margin-top: 2px; text-transform: uppercase;
}
.seo-field { margin-bottom: 0.75rem; }
hr.forge-divider { border: none; border-top: 1px solid var(--border); margin: 1rem 0; }
.prompt-pill {
    display: inline-block; background: var(--surface3);
    border: 1px solid var(--border2); border-radius: 100px;
    padding: 0.2rem 0.75rem; margin: 0.2rem;
    font-size: 0.75rem; color: var(--muted); cursor: pointer;
    transition: all 0.15s;
}
.prompt-pill:hover { border-color: var(--accent); color: var(--accent); }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# HELPER / UTIL FUNCTIONS
# ═══════════════════════════════════════════════════════

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    try:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    except:
        return (108, 99, 255)

def luminance(hex_color):
    r, g, b = hex_to_rgb(hex_color)
    return (r * 0.299 + g * 0.587 + b * 0.114) / 255

def is_dark_color(hex_color):
    return luminance(hex_color) < 0.5

def contrast_color(hex_color):
    return "#000000" if luminance(hex_color) > 0.55 else "#ffffff"

def color_mix(hex1, hex2, ratio=0.5):
    r1, g1, b1 = hex_to_rgb(hex1)
    r2, g2, b2 = hex_to_rgb(hex2)
    r = int(r1 * ratio + r2 * (1 - ratio))
    g = int(g1 * ratio + g2 * (1 - ratio))
    b = int(b1 * ratio + b2 * (1 - ratio))
    return f"#{r:02x}{g:02x}{b:02x}"

def estimate_word_count(data):
    text = " ".join([
        data.get('headline', ''),
        data.get('subheadline', ''),
        data.get('hero_body', ''),
        " ".join([f.get('desc', '') for f in data.get('features', [])]),
        " ".join([t.get('text', '') for t in data.get('testimonials', [])]),
        " ".join([f"{i.get('q','')} {i.get('a','')}" for i in data.get('faq', [])]),
    ])
    return len(text.split())

def score_copy(data):
    """Heuristic copy quality scores 0-100"""
    scores = {}
    headline = data.get('headline', '')
    scores['headline'] = min(100, max(0, 60 + (10 if len(headline.split()) <= 8 else 0) + (15 if any(w in headline.lower() for w in ['transform','revolutionize','unlock','power','master','crush','dominate','effortless','ultimate']) else 0) + (15 if '?' not in headline and '!' not in headline else -5)))
    hero = data.get('hero_body', '')
    scores['hero'] = min(100, max(0, 40 + len(hero.split()) * 0.4))
    scores['features'] = min(100, max(0, len(data.get('features', [])) * 14))
    scores['social_proof'] = min(100, max(0, (50 if data.get('testimonials') else 0) + (25 if data.get('stats') else 0) + (25 if data.get('social_proof') else 0)))
    scores['completeness'] = min(100, max(0, sum([
        20 if data.get('headline') else 0,
        15 if data.get('hero_body') else 0,
        20 if len(data.get('features', [])) >= 4 else 10 if data.get('features') else 0,
        15 if data.get('testimonials') else 0,
        15 if data.get('faq') else 0,
        15 if data.get('stats') else 0,
    ])))
    overall = int(sum(scores.values()) / len(scores))
    return scores, overall

def call_openai(prompt, api_key, model, max_tokens=4000, system=None, temperature=0.8):
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
            model=model, messages=messages,
            temperature=temperature, max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"❌ OpenAI Error: {str(e)}")
        return None

def extract_json(text):
    if not text:
        return None
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass
    return None

# ═══════════════════════════════════════════════════════
# AI GENERATION FUNCTIONS
# ═══════════════════════════════════════════════════════

def generate_full_page(description, tone, industry, audience, lang, framework, api_key, model):
    system = """You are the world's best conversion copywriter and digital marketing strategist.
You write copy that converts. You understand psychology, persuasion, and UX deeply.
Return ONLY valid JSON. No markdown fences, no extra text whatsoever."""

    prompt = f"""Create a complete, conversion-optimized landing page for:

BUSINESS: {description}
TONE: {tone}
INDUSTRY: {industry}
AUDIENCE: {audience}
LANGUAGE: {lang}
FRAMEWORK/VIBE: {framework}

Return this EXACT JSON structure (all fields required):
{{
  "brand_name": "Short memorable brand name",
  "tagline": "3-6 word brand tagline",
  "headline": "Powerful 6-9 word headline using active verbs and power words",
  "subheadline": "14-20 word value prop subheadline with specificity",
  "hero_body": "2-3 sentence emotional hook: address pain point, promise transformation, build urgency. 60-90 words.",
  "cta_primary": "2-4 word action CTA",
  "cta_secondary": "2-4 word softer CTA",
  "email_placeholder": "Contextual email placeholder text",
  "social_proof": "Compact social proof like: Trusted by 12,000+ marketers worldwide",
  "nav_links": ["Link1","Link2","Link3","Link4","Link5"],
  "features": [
    {{"icon":"⚡","title":"Feature Name","desc":"25-35 word benefit-focused description emphasizing outcome not feature"}},
    {{"icon":"🎯","title":"Feature Name","desc":"25-35 word benefit-focused description emphasizing outcome not feature"}},
    {{"icon":"🔥","title":"Feature Name","desc":"25-35 word benefit-focused description emphasizing outcome not feature"}},
    {{"icon":"💎","title":"Feature Name","desc":"25-35 word benefit-focused description emphasizing outcome not feature"}},
    {{"icon":"🚀","title":"Feature Name","desc":"25-35 word benefit-focused description emphasizing outcome not feature"}},
    {{"icon":"✨","title":"Feature Name","desc":"25-35 word benefit-focused description emphasizing outcome not feature"}},
    {{"icon":"🛡️","title":"Feature Name","desc":"25-35 word benefit-focused description emphasizing outcome not feature"}},
    {{"icon":"📈","title":"Feature Name","desc":"25-35 word benefit-focused description emphasizing outcome not feature"}}
  ],
  "stats": [
    {{"num":"10k+","label":"Happy Users","icon":"👥"}},
    {{"num":"98%","label":"Satisfaction","icon":"⭐"}},
    {{"num":"3x","label":"Avg ROI","icon":"📈"}},
    {{"num":"24/7","label":"Support","icon":"🛡️"}}
  ],
  "testimonials": [
    {{"name":"Jane Smith","role":"CEO, TechCorp","text":"40-50 word specific testimonial with measurable result mentioned","rating":5,"company_size":"Series B startup"}},
    {{"name":"Marcus Lee","role":"Marketing Director, Acme","text":"40-50 word specific testimonial with measurable result mentioned","rating":5,"company_size":"Fortune 500"}},
    {{"name":"Priya Patel","role":"Founder, GrowthLab","text":"40-50 word specific testimonial with measurable result mentioned","rating":5,"company_size":"Bootstrapped"}}
  ],
  "pricing": [
    {{"name":"Starter","price":"$29","period":"/mo","desc":"Perfect for individuals and small teams","highlight":false,"cta":"Start Free","features":["Feature A","Feature B","Feature C","Feature D"]}},
    {{"name":"Pro","price":"$79","period":"/mo","desc":"For growing teams that need more power","highlight":true,"cta":"Start Free Trial","badge":"Most Popular","features":["Everything in Starter","Feature E","Feature F","Feature G","Feature H"]}},
    {{"name":"Enterprise","price":"Custom","period":"","desc":"Full-featured for large organizations","highlight":false,"cta":"Contact Sales","features":["Everything in Pro","Feature I","Feature J","Feature K","Dedicated Support"]}}
  ],
  "faq": [
    {{"q":"Most common first question about getting started?","a":"35-45 word clear, confident answer that removes friction"}},
    {{"q":"Question about pricing or value?","a":"35-45 word clear, confident answer that removes friction"}},
    {{"q":"Question about security or trust?","a":"35-45 word clear, confident answer that removes friction"}},
    {{"q":"Question about results or timeline?","a":"35-45 word clear, confident answer that removes friction"}},
    {{"q":"Question about integration or compatibility?","a":"35-45 word clear, confident answer that removes friction"}},
    {{"q":"Question about cancellation or commitment?","a":"35-45 word clear, confident answer that removes friction"}}
  ],
  "process_steps": [
    {{"step":"01","title":"Step Name","desc":"20-30 word description of this step"}},
    {{"step":"02","title":"Step Name","desc":"20-30 word description of this step"}},
    {{"step":"03","title":"Step Name","desc":"20-30 word description of this step"}},
    {{"step":"04","title":"Step Name","desc":"20-30 word description of this step"}}
  ],
  "logos": ["Google","Microsoft","Shopify","Stripe","Notion","Figma","HubSpot","Slack"],
  "guarantee": "30-day money-back guarantee — no questions asked",
  "urgency_text": "Short urgency line like: Limited time offer — 40% off for first 200 users",
  "footer_text": "Short inspiring footer tagline",
  "seo_title": "SEO-optimized page title under 60 chars",
  "seo_description": "SEO meta description 140-155 chars",
  "seo_keywords": ["keyword1","keyword2","keyword3","keyword4","keyword5"]
}}"""

    raw = call_openai(prompt, api_key, model, 5000, system)
    return extract_json(raw)

def regenerate_section(section, context, api_key, model, tone="Professional"):
    system = "You are an elite copywriter. Return ONLY valid JSON, no extra text."
    prompts = {
        "headline": f"""Write 5 alternative powerful headlines for: {context}\nTone: {tone}\nReturn: {{"options":["h1","h2","h3","h4","h5"]}}""",
        "hero_body": f"""Write 3 alternative hero body paragraphs (60-90 words each) for: {context}\nTone: {tone}\nReturn: {{"options":["p1","p2","p3"]}}""",
        "features": f"""Write 8 compelling features for: {context}\nTone: {tone}\nReturn: {{"features":[{{"icon":"⚡","title":"T","desc":"D"}}]}}""",
        "testimonials": f"""Write 3 realistic testimonials for: {context}\nReturn: {{"testimonials":[{{"name":"N","role":"R","text":"T","rating":5,"company_size":"S"}}]}}""",
        "faq": f"""Write 6 FAQ items for: {context}\nReturn: {{"faq":[{{"q":"Q","a":"A"}}]}}""",
        "cta": f"""Write 6 compelling CTA options for: {context}\nTone: {tone}\nReturn: {{"options":["c1","c2","c3","c4","c5","c6"]}}""",
        "pricing": f"""Write 3 pricing tier options for: {context}\nReturn: {{"pricing":[{{"name":"N","price":"$X","period":"/mo","desc":"D","highlight":false,"cta":"C","features":["F1","F2"]}}]}}""",
        "stats": f"""Write 4 impressive stats for: {context}\nReturn: {{"stats":[{{"num":"N","label":"L","icon":"I"}}]}}""",
        "process": f"""Write 4 process steps for: {context}\nReturn: {{"steps":[{{"step":"01","title":"T","desc":"D"}}]}}""",
    }
    raw = call_openai(prompts.get(section, ""), api_key, model, 2000, system)
    return extract_json(raw)

def generate_ab_variant(data, api_key, model):
    system = "You are an elite CRO specialist. Return ONLY valid JSON, no extra text."
    prompt = f"""Create an A/B test variant for this landing page content.
Change the messaging angle significantly — different emotional hook, different value prop framing.

Current headline: {data.get('headline')}
Current hero: {data.get('hero_body')}
Business: {data.get('brand_name')}

Return: {{
  "headline": "new headline",
  "subheadline": "new subheadline",
  "hero_body": "new hero body 60-90 words",
  "cta_primary": "new CTA",
  "variant_rationale": "2-3 sentences explaining the different angle this variant takes"
}}"""
    raw = call_openai(prompt, api_key, model, 1500, system)
    return extract_json(raw)

def generate_seo_meta(data, api_key, model):
    system = "You are an SEO expert. Return ONLY valid JSON."
    prompt = f"""Generate comprehensive SEO metadata for:
Brand: {data.get('brand_name')}
Headline: {data.get('headline')}
Description: {data.get('hero_body')}

Return: {{
  "seo_title": "under 60 chars",
  "seo_description": "140-155 chars",
  "og_title": "Open Graph title",
  "og_description": "Open Graph description",
  "twitter_title": "Twitter card title",
  "twitter_description": "Twitter card description",
  "seo_keywords": ["kw1","kw2","kw3","kw4","kw5","kw6","kw7","kw8"],
  "schema_type": "SoftwareApplication or Service or Product",
  "canonical_slug": "url-friendly-slug"
}}"""
    raw = call_openai(prompt, api_key, model, 1000, system)
    return extract_json(raw)

def generate_email_sequence(data, api_key, model):
    system = "You are an email marketing expert. Return ONLY valid JSON."
    prompt = f"""Write a 3-email welcome sequence for:
Product: {data.get('brand_name')} — {data.get('headline')}
Target: new signups

Return: {{
  "emails": [
    {{"subject":"Welcome subject line","preview":"Preview text","body":"150-word email body","cta":"CTA text"}},
    {{"subject":"Day 3 subject line","preview":"Preview text","body":"150-word email body","cta":"CTA text"}},
    {{"subject":"Day 7 subject line","preview":"Preview text","body":"150-word email body","cta":"CTA text"}}
  ]
}}"""
    raw = call_openai(prompt, api_key, model, 2000, system)
    return extract_json(raw)

def generate_social_copy(data, api_key, model):
    system = "You are a social media expert. Return ONLY valid JSON."
    prompt = f"""Write social media posts for:
Product: {data.get('brand_name')} — {data.get('headline')}
Value: {data.get('hero_body', '')[:200]}

Return: {{
  "twitter": ["tweet1 (max 240 chars)", "tweet2", "tweet3"],
  "linkedin": "Professional LinkedIn post 150-200 words with hashtags",
  "instagram_caption": "Engaging Instagram caption with emojis and hashtags",
  "product_hunt_tagline": "One-line Product Hunt tagline under 60 chars",
  "reddit_title": "Casual Reddit post title"
}}"""
    raw = call_openai(prompt, api_key, model, 1500, system)
    return extract_json(raw)

def generate_ad_copy(data, api_key, model):
    system = "You are a PPC ad specialist. Return ONLY valid JSON."
    prompt = f"""Write ad copy for:
Product: {data.get('brand_name')} — {data.get('headline')}
Value: {data.get('subheadline', '')}

Return: {{
  "google_ads": [
    {{"headline1":"30 chars max","headline2":"30 chars max","headline3":"30 chars max","desc1":"90 chars max","desc2":"90 chars max"}},
    {{"headline1":"30 chars max","headline2":"30 chars max","headline3":"30 chars max","desc1":"90 chars max","desc2":"90 chars max"}}
  ],
  "facebook": {{
    "primary_text": "125 char primary text",
    "headline": "40 char headline",
    "description": "30 char description"
  }},
  "display_banner": "Short punchy display ad text under 25 words"
}}"""
    raw = call_openai(prompt, api_key, model, 1500, system)
    return extract_json(raw)


# ═══════════════════════════════════════════════════════
# HTML GENERATION (FULL PRODUCTION PAGE)
# ═══════════════════════════════════════════════════════

def build_html(data, s):
    brand   = s.get('brand_color','#6c63ff')
    accent  = s.get('accent_color','#ff6584')
    bg      = s.get('bg_color','#0d0d18')
    text    = s.get('text_color','#f0f0ff')
    cta_url = s.get('cta_url','#signup')
    font    = s.get('font_pair','Modern')
    hero_lay= s.get('hero_layout','Centered')
    anim    = s.get('animation_style','Smooth')
    bg_fx   = s.get('bg_effect','Gradient Mesh')
    dark    = is_dark_color(bg)
    brand_r, brand_g, brand_b = hex_to_rgb(brand)
    acc_r, acc_g, acc_b = hex_to_rgb(accent)
    bg_r, bg_g, bg_b = hex_to_rgb(bg)
    cta_txt_color = contrast_color(brand)
    surface_color = f"rgba({brand_r},{brand_g},{brand_b},{'0.06' if dark else '0.04'})"
    border_col = f"rgba({'255,255,255' if dark else '0,0,0'},{'0.1' if dark else '0.1'})"
    muted_col  = f"rgba({'255,255,255' if dark else '0,0,0'},{'0.5' if dark else '0.45'})"

    FONTS = {
        'Modern':     ('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap', "'Syne',sans-serif", "'DM Sans',sans-serif"),
        'Editorial':  ('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Lato:wght@300;400;700&display=swap', "'Playfair Display',serif", "'Lato',sans-serif"),
        'Technical':  ('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap', "'IBM Plex Mono',monospace", "'IBM Plex Sans',sans-serif"),
        'Elegant':    ('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;1,400&family=Josefin+Sans:wght@300;400;600&display=swap', "'Cormorant Garamond',serif", "'Josefin Sans',sans-serif"),
        'Bold':       ('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500&display=swap', "'Bebas Neue',display", "'Inter',sans-serif"),
        'Futuristic': ('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap', "'Orbitron',sans-serif", "'Rajdhani',sans-serif"),
        'Humanist':   ('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;600&display=swap', "'Fraunces',serif", "'Plus Jakarta Sans',sans-serif"),
        'Retro':      ('https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Nunito:wght@300;400;700&display=swap', "'Alfa Slab One',serif", "'Nunito',sans-serif"),
    }
    fimport, hfont, bfont = FONTS.get(font, FONTS['Modern'])

    # BG EFFECT
    bg_css = {
        'Gradient Mesh': f"background: radial-gradient(ellipse at 0% 0%, rgba({brand_r},{brand_g},{brand_b},0.15) 0%, transparent 55%), radial-gradient(ellipse at 100% 100%, rgba({acc_r},{acc_g},{acc_b},0.12) 0%, transparent 55%), {bg};",
        'Dots':  f"background-color:{bg}; background-image:radial-gradient(circle, rgba({brand_r},{brand_g},{brand_b},0.12) 1px, transparent 1px); background-size:28px 28px;",
        'Grid':  f"background-color:{bg}; background-image:linear-gradient(rgba({brand_r},{brand_g},{brand_b},0.06) 1px, transparent 1px), linear-gradient(90deg, rgba({brand_r},{brand_g},{brand_b},0.06) 1px, transparent 1px); background-size:40px 40px;",
        'Lines': f"background-color:{bg}; background-image:repeating-linear-gradient(0deg, rgba({brand_r},{brand_g},{brand_b},0.05) 0px, rgba({brand_r},{brand_g},{brand_b},0.05) 1px, transparent 1px, transparent 40px);",
        'Diagonal': f"background-color:{bg}; background-image:repeating-linear-gradient(45deg, rgba({brand_r},{brand_g},{brand_b},0.04) 0px, rgba({brand_r},{brand_g},{brand_b},0.04) 1px, transparent 0, transparent 50%); background-size:20px 20px;",
        'Solid': f"background-color:{bg};",
        'Gradient': f"background: linear-gradient(135deg, {bg} 0%, {color_mix(bg, brand, 0.8)} 100%);",
    }.get(bg_fx, f"background-color:{bg};")

    # ANIMATION CSS
    anim_css = {
        'Smooth': "@keyframes fadeUp{from{opacity:0;transform:translateY(28px)}to{opacity:1;transform:translateY(0)}} @keyframes fadeIn{from{opacity:0}to{opacity:1}} .au{animation:fadeUp 0.7s ease both} .af{animation:fadeIn 0.6s ease both} .d1{animation-delay:0.1s} .d2{animation-delay:0.2s} .d3{animation-delay:0.3s} .d4{animation-delay:0.4s} .d5{animation-delay:0.5s} .d6{animation-delay:0.6s} .d7{animation-delay:0.7s} .d8{animation-delay:0.8s}",
        'Dramatic': "@keyframes zoomIn{from{opacity:0;transform:scale(0.88)}to{opacity:1;transform:scale(1)}} @keyframes slideUp{from{opacity:0;transform:translateY(50px)}to{opacity:1;transform:translateY(0)}} .au{animation:zoomIn 0.9s cubic-bezier(0.16,1,0.3,1) both} .af{animation:zoomIn 0.7s ease both} .d1{animation-delay:0.15s} .d2{animation-delay:0.3s} .d3{animation-delay:0.45s} .d4{animation-delay:0.6s} .d5{animation-delay:0.75s} .d6{animation-delay:0.9s} .d7{animation-delay:1.05s} .d8{animation-delay:1.2s}",
        'Typewriter': "@keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}} .au{animation:fadeUp 0.5s ease both} .af{animation:fadeUp 0.4s ease both} .d1{animation-delay:0.05s} .d2{animation-delay:0.15s} .d3{animation-delay:0.25s} .d4{animation-delay:0.35s} .d5{animation-delay:0.45s} .d6{animation-delay:0.55s} .d7{animation-delay:0.65s} .d8{animation-delay:0.75s}",
        'None': ".au,.af{} .d1,.d2,.d3,.d4,.d5,.d6,.d7,.d8{}",
    }.get(anim, '')

    # ─── SECTIONS ───

    # NAV
    nav = ""
    if s.get('show_nav', True):
        sticky = "position:sticky;top:0;z-index:1000;" if s.get('nav_sticky', True) else ""
        nav_links = " ".join([f'<a href="#{l.lower()}">{l}</a>' for l in data.get('nav_links',['Features','Pricing','FAQ'])])
        nav = f"""<nav style="{sticky}background:{'rgba(7,8,15,0.88)' if dark else 'rgba(255,255,255,0.88)'};backdrop-filter:blur(20px);border-bottom:1px solid {border_col};">
<div class="ctr" style="display:flex;align-items:center;gap:2rem;height:64px;">
  <div style="font-family:{hfont};font-size:1.3rem;font-weight:800;color:{brand};flex-shrink:0;letter-spacing:0.04em;">{data.get('brand_name','Brand')}</div>
  <div class="nav-links" style="display:flex;gap:1.5rem;flex:1;">{nav_links}</div>
  <a href="{cta_url}" style="background:{brand};color:{cta_txt_color};padding:0.5rem 1.2rem;border-radius:7px;text-decoration:none;font-weight:700;font-size:0.85rem;transition:all 0.2s;flex-shrink:0;">{data.get('cta_primary','Get Started')}</a>
  <button onclick="document.querySelector('.nav-links').classList.toggle('open')" style="display:none;background:none;border:none;color:{text};font-size:1.5rem;cursor:pointer;" class="hamburger">☰</button>
</div></nav>"""

    # HERO BADGE / URGENCY
    urgency = data.get('urgency_text', '')
    urgency_bar = f"""<div style="background:linear-gradient(90deg,{brand},{accent});padding:0.5rem;text-align:center;font-size:0.82rem;font-weight:600;color:{cta_txt_color};letter-spacing:0.04em;">
  {urgency} <a href="{cta_url}" style="color:{cta_txt_color};text-decoration:underline;margin-left:0.5rem;">Claim now →</a>
</div>""" if urgency and s.get('show_urgency', True) else ""

    badge_html = f'<div class="au" style="display:inline-flex;align-items:center;gap:0.4rem;background:rgba({brand_r},{brand_g},{brand_b},0.12);border:1px solid rgba({brand_r},{brand_g},{brand_b},0.3);color:{brand};padding:0.3rem 1rem;border-radius:100px;font-size:0.8rem;font-weight:600;margin-bottom:1.25rem;">{data.get("social_proof","")}</div>'

    # HERO
    if hero_lay == 'Centered':
        hero = f"""<section style="padding:90px 0 70px;position:relative;overflow:hidden;text-align:center;">
  <div style="position:absolute;top:-150px;left:50%;transform:translateX(-50%);width:700px;height:700px;background:radial-gradient(circle,rgba({brand_r},{brand_g},{brand_b},0.13) 0%,transparent 65%);pointer-events:none;"></div>
  <div class="ctr" style="max-width:820px;">
    {badge_html}
    <h1 class="au d1" style="font-family:{hfont};font-size:clamp(2.6rem,6vw,4.8rem);font-weight:800;line-height:1.08;letter-spacing:-0.025em;margin-bottom:1.1rem;background:linear-gradient(135deg,{text} 30%,{brand} 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">{data.get('headline','Your Headline')}</h1>
    <p class="au d2" style="font-size:1.18rem;color:{muted_col};margin-bottom:0.8rem;font-weight:400;line-height:1.5;">{data.get('subheadline','')}</p>
    <p class="au d3" style="font-size:1rem;color:{muted_col};margin-bottom:2rem;line-height:1.75;max-width:620px;margin-left:auto;margin-right:auto;">{data.get('hero_body','')}</p>
    <div class="au d4" style="display:flex;gap:0.75rem;justify-content:center;flex-wrap:wrap;margin-bottom:1.25rem;">
      <a href="{cta_url}" style="background:{brand};color:{cta_txt_color};padding:0.85rem 2rem;border-radius:8px;text-decoration:none;font-weight:700;font-size:0.95rem;box-shadow:0 4px 18px rgba({brand_r},{brand_g},{brand_b},0.38);transition:all 0.2s;">{data.get('cta_primary','Get Started')}</a>
      <a href="#features" style="border:1.5px solid {border_col};color:{text};padding:0.85rem 2rem;border-radius:8px;text-decoration:none;font-weight:600;font-size:0.95rem;background:{surface_color};transition:all 0.2s;">{data.get('cta_secondary','See How It Works')}</a>
    </div>
    <div class="au d5" style="display:flex;gap:0.5rem;max-width:420px;margin:0 auto;padding:0.35rem;background:{surface_color};border:1px solid {border_col};border-radius:10px;">
      <input type="email" placeholder="{data.get('email_placeholder','your@email.com')}" style="flex:1;background:none;border:none;outline:none;color:{text};font-size:0.9rem;padding:0.4rem 0.7rem;">
      <button style="background:{brand};color:{cta_txt_color};border:none;padding:0.5rem 1.2rem;border-radius:7px;font-weight:700;cursor:pointer;font-size:0.85rem;">{data.get('cta_primary','Start Free')}</button>
    </div>
  </div>
</section>"""

    elif hero_lay == 'Split':
        hero = f"""<section style="padding:70px 0 50px;position:relative;overflow:hidden;">
  <div class="ctr" style="display:grid;grid-template-columns:1fr 1fr;gap:4rem;align-items:center;">
    <div>
      {badge_html}
      <h1 class="au d1" style="font-family:{hfont};font-size:clamp(2rem,5vw,3.6rem);font-weight:800;line-height:1.1;letter-spacing:-0.025em;margin-bottom:1rem;background:linear-gradient(135deg,{text} 30%,{brand} 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">{data.get('headline','')}</h1>
      <p class="au d2" style="font-size:1.1rem;color:{muted_col};margin-bottom:0.75rem;">{data.get('subheadline','')}</p>
      <p class="au d3" style="font-size:0.97rem;color:{muted_col};margin-bottom:1.75rem;line-height:1.75;">{data.get('hero_body','')}</p>
      <div class="au d4" style="display:flex;gap:0.75rem;flex-wrap:wrap;">
        <a href="{cta_url}" style="background:{brand};color:{cta_txt_color};padding:0.8rem 1.8rem;border-radius:8px;text-decoration:none;font-weight:700;font-size:0.9rem;box-shadow:0 4px 18px rgba({brand_r},{brand_g},{brand_b},0.35);">{data.get('cta_primary','Get Started')}</a>
        <a href="#features" style="border:1.5px solid {border_col};color:{text};padding:0.8rem 1.8rem;border-radius:8px;text-decoration:none;font-weight:600;font-size:0.9rem;background:{surface_color};">{data.get('cta_secondary','Learn More')} →</a>
      </div>
    </div>
    <div class="au d3">
      <div style="background:{surface_color};border:1px solid {border_col};border-radius:16px;overflow:hidden;box-shadow:0 24px 60px rgba(0,0,0,0.35);">
        <div style="display:flex;gap:6px;padding:12px 16px;background:rgba({'255,255,255' if dark else '0,0,0'},0.04);border-bottom:1px solid {border_col};">
          <span style="width:10px;height:10px;border-radius:50%;background:#ff5f57;display:inline-block;"></span>
          <span style="width:10px;height:10px;border-radius:50%;background:#febc2e;display:inline-block;"></span>
          <span style="width:10px;height:10px;border-radius:50%;background:#28c840;display:inline-block;"></span>
        </div>
        <div style="padding:20px;display:flex;flex-direction:column;gap:12px;">
          <div style="height:10px;background:{border_col};border-radius:4px;width:100%;"></div>
          <div style="height:10px;background:{border_col};border-radius:4px;width:72%;"></div>
          <div style="height:10px;background:{border_col};border-radius:4px;width:48%;"></div>
          <div style="height:80px;background:linear-gradient(135deg,rgba({brand_r},{brand_g},{brand_b},0.18),rgba({acc_r},{acc_g},{acc_b},0.12));border:1px solid rgba({brand_r},{brand_g},{brand_b},0.2);border-radius:8px;"></div>
          <div style="display:flex;gap:10px;">
            <div style="height:60px;flex:1;background:linear-gradient(135deg,rgba({brand_r},{brand_g},{brand_b},0.12),rgba({acc_r},{acc_g},{acc_b},0.08));border:1px solid {border_col};border-radius:8px;"></div>
            <div style="height:60px;flex:1;background:linear-gradient(135deg,rgba({acc_r},{acc_g},{acc_b},0.12),rgba({brand_r},{brand_g},{brand_b},0.08));border:1px solid {border_col};border-radius:8px;"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>"""

    elif hero_lay == 'Minimal':
        hero = f"""<section style="padding:120px 0 80px;">
  <div class="ctr">
    <p class="au" style="font-size:0.72rem;letter-spacing:0.22em;text-transform:uppercase;color:{brand};font-weight:700;margin-bottom:1rem;">{data.get('tagline','')}</p>
    <h1 class="au d1" style="font-family:{hfont};font-size:clamp(3.5rem,9vw,8rem);font-weight:800;line-height:1.0;letter-spacing:-0.035em;margin-bottom:1.5rem;">{data.get('headline','')}</h1>
    <div style="width:60px;height:3px;background:{brand};margin-bottom:1.5rem;"></div>
    <p class="au d2" style="font-size:1.1rem;color:{muted_col};max-width:560px;line-height:1.7;margin-bottom:2rem;">{data.get('subheadline','')}</p>
    <div class="au d3" style="display:flex;gap:0.75rem;flex-wrap:wrap;">
      <a href="{cta_url}" style="background:{brand};color:{cta_txt_color};padding:0.85rem 2rem;border-radius:8px;text-decoration:none;font-weight:700;font-size:0.95rem;box-shadow:0 4px 18px rgba({brand_r},{brand_g},{brand_b},0.35);">{data.get('cta_primary','Get Started')}</a>
      <a href="#features" style="border:1.5px solid {border_col};color:{text};padding:0.85rem 2rem;border-radius:8px;text-decoration:none;font-weight:600;font-size:0.95rem;">{data.get('cta_secondary','Learn More')} →</a>
    </div>
  </div>
</section>"""

    elif hero_lay == 'Magazine':
        hero = f"""<section style="padding:0;min-height:90vh;display:grid;grid-template-columns:1fr 1fr;">
  <div style="padding:80px 60px;display:flex;flex-direction:column;justify-content:center;">
    {badge_html}
    <h1 class="au d1" style="font-family:{hfont};font-size:clamp(2.5rem,5vw,5rem);font-weight:800;line-height:1.0;letter-spacing:-0.03em;margin-bottom:1rem;">{data.get('headline','')}</h1>
    <div style="width:40px;height:4px;background:{brand};margin:1rem 0;"></div>
    <p class="au d2" style="font-size:1rem;color:{muted_col};line-height:1.75;margin-bottom:1.5rem;">{data.get('hero_body','')}</p>
    <a href="{cta_url}" class="au d3" style="display:inline-flex;align-items:center;gap:0.5rem;background:{brand};color:{cta_txt_color};padding:0.85rem 2rem;border-radius:8px;text-decoration:none;font-weight:700;font-size:0.95rem;align-self:flex-start;">{data.get('cta_primary','Get Started')} →</a>
  </div>
  <div style="background:linear-gradient(135deg,rgba({brand_r},{brand_g},{brand_b},0.2) 0%,rgba({acc_r},{acc_g},{acc_b},0.15) 100%);display:flex;align-items:center;justify-content:center;font-size:6rem;border-left:1px solid {border_col};">🚀</div>
</section>"""

    else:  # Video
        hero = f"""<section style="padding:90px 0 70px;text-align:center;position:relative;overflow:hidden;">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba({brand_r},{brand_g},{brand_b},0.08) 0%,transparent 100%);pointer-events:none;"></div>
  <div class="ctr" style="max-width:800px;">
    {badge_html}
    <h1 class="au d1" style="font-family:{hfont};font-size:clamp(2.5rem,6vw,5rem);font-weight:800;line-height:1.08;letter-spacing:-0.025em;margin-bottom:1rem;">{data.get('headline','')}</h1>
    <p class="au d2" style="font-size:1.1rem;color:{muted_col};margin-bottom:2rem;">{data.get('subheadline','')}</p>
    <div class="au d3" style="background:{surface_color};border:1px solid {border_col};border-radius:16px;padding:3rem;margin-bottom:2rem;cursor:pointer;position:relative;" onclick="this.innerHTML='<p style=text-align:center;color:{muted_col};padding:1rem>▶ Video would play here</p>'">
      <div style="font-size:4rem;margin-bottom:0.5rem;">▶</div>
      <p style="color:{muted_col};font-size:0.9rem;">Watch 2-min demo</p>
    </div>
    <div class="au d4" style="display:flex;gap:0.75rem;justify-content:center;">
      <a href="{cta_url}" style="background:{brand};color:{cta_txt_color};padding:0.85rem 2rem;border-radius:8px;text-decoration:none;font-weight:700;font-size:0.95rem;box-shadow:0 4px 18px rgba({brand_r},{brand_g},{brand_b},0.35);">{data.get('cta_primary','Get Started')}</a>
    </div>
  </div>
</section>"""

    # LOGO BAR
    logo_bar = ""
    if s.get('show_logos', True) and data.get('logos'):
        logos_html = " ".join([f'<span style="font-weight:700;font-size:0.9rem;color:{muted_col};letter-spacing:0.06em;text-transform:uppercase;">{l}</span>' for l in data.get('logos',[])])
        logo_bar = f"""<section style="padding:40px 0;border-top:1px solid {border_col};border-bottom:1px solid {border_col};">
  <div class="ctr" style="text-align:center;">
    <p style="font-size:0.72rem;letter-spacing:0.16em;text-transform:uppercase;color:{muted_col};margin-bottom:1.5rem;">TRUSTED BY TEAMS AT</p>
    <div style="display:flex;gap:2.5rem;justify-content:center;flex-wrap:wrap;align-items:center;">{logos_html}</div>
  </div>
</section>"""

    # STATS
    stats_html = ""
    if s.get('show_stats', True) and data.get('stats'):
        stat_items = " ".join([f'<div style="text-align:center;"><div style="font-size:0.4rem;margin-bottom:0.25rem;">{st.get("icon","")}</div><div style="font-family:{hfont};font-size:2.8rem;font-weight:800;color:{brand};letter-spacing:0.02em;line-height:1;">{st["num"]}</div><div style="font-size:0.78rem;color:{muted_col};text-transform:uppercase;letter-spacing:0.1em;font-weight:600;margin-top:0.3rem;">{st["label"]}</div></div>' for st in data.get('stats',[])])
        stats_html = f"""<section style="padding:70px 0;"><div class="ctr"><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:2rem;">{stat_items}</div></div></section>"""

    # FEATURES
    features_html = ""
    if s.get('show_features', True) and data.get('features'):
        feats = data['features']
        cards = ""
        for i, f in enumerate(feats):
            d_cls = f"d{min(i+1,8)}"
            cards += f"""<div class="au {d_cls}" style="background:{surface_color};border:1px solid {border_col};border-radius:12px;padding:1.75rem;transition:all 0.3s ease;position:relative;overflow:hidden;" onmouseenter="this.style.borderColor='rgba({brand_r},{brand_g},{brand_b},0.4)';this.style.transform='translateY(-4px)';" onmouseleave="this.style.borderColor='{border_col}';this.style.transform='translateY(0)';">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,{brand},{accent});opacity:0;transition:opacity 0.3s;" class="feat-top"></div>
  <div style="font-size:1.8rem;margin-bottom:0.9rem;">{f.get('icon','⚡')}</div>
  <h3 style="font-family:{hfont};font-size:1.1rem;font-weight:700;margin-bottom:0.5rem;color:{text};">{f.get('title','')}</h3>
  <p style="font-size:0.88rem;color:{muted_col};line-height:1.65;">{f.get('desc','')}</p>
</div>"""
        grid_cols = "repeat(4,1fr)" if len(feats) >= 8 else "repeat(3,1fr)" if len(feats) >= 5 else "repeat(2,1fr)"
        features_html = f"""<section id="features" style="padding:100px 0;">
  <div class="ctr">
    <div style="text-align:center;margin-bottom:4rem;">
      <span style="display:inline-block;font-size:0.72rem;letter-spacing:0.2em;text-transform:uppercase;color:{brand};font-weight:700;margin-bottom:0.75rem;padding:0.25rem 0.75rem;background:rgba({brand_r},{brand_g},{brand_b},0.1);border-radius:100px;">Features</span>
      <h2 style="font-family:{hfont};font-size:clamp(2rem,4vw,3rem);font-weight:800;letter-spacing:-0.02em;line-height:1.2;">Everything you need to <em style="font-style:normal;color:{brand};">succeed</em></h2>
    </div>
    <div style="display:grid;grid-template-columns:{grid_cols};gap:1.25rem;">{cards}</div>
  </div>
</section>"""

    # PROCESS
    process_html = ""
    if s.get('show_process', True) and data.get('process_steps'):
        steps = data['process_steps']
        step_items = ""
        for i, step in enumerate(steps):
            connector = f'<div style="position:absolute;top:24px;left:calc(50% + 30px);width:calc(100% - 60px);height:1px;background:linear-gradient(90deg,{border_col},transparent);"></div>' if i < len(steps)-1 else ''
            step_items += f"""<div style="text-align:center;position:relative;">
  {connector}
  <div style="width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,{brand},{accent});display:flex;align-items:center;justify-content:center;font-family:{hfont};font-size:1.1rem;font-weight:800;color:{cta_txt_color};margin:0 auto 1rem;">{step.get('step','01')}</div>
  <h3 style="font-family:{hfont};font-size:1.05rem;font-weight:700;margin-bottom:0.5rem;">{step.get('title','')}</h3>
  <p style="font-size:0.85rem;color:{muted_col};line-height:1.6;">{step.get('desc','')}</p>
</div>"""
        process_html = f"""<section id="how-it-works" style="padding:90px 0;background:{surface_color};">
  <div class="ctr">
    <div style="text-align:center;margin-bottom:4rem;">
      <span style="display:inline-block;font-size:0.72rem;letter-spacing:0.2em;text-transform:uppercase;color:{brand};font-weight:700;margin-bottom:0.75rem;padding:0.25rem 0.75rem;background:rgba({brand_r},{brand_g},{brand_b},0.1);border-radius:100px;">How It Works</span>
      <h2 style="font-family:{hfont};font-size:clamp(2rem,4vw,3rem);font-weight:800;letter-spacing:-0.02em;">Up and running in <em style="font-style:normal;color:{brand};">minutes</em></h2>
    </div>
    <div style="display:grid;grid-template-columns:repeat({len(steps)},1fr);gap:2rem;">{step_items}</div>
  </div>
</section>"""

    # TESTIMONIALS
    testimonials_html = ""
    if s.get('show_testimonials', True) and data.get('testimonials'):
        cards_t = ""
        for t in data.get('testimonials', []):
            stars = "★" * t.get('rating', 5)
            cards_t += f"""<div style="background:{'rgba(255,255,255,0.03)' if dark else 'rgba(255,255,255,0.85)'};border:1px solid {border_col};border-radius:12px;padding:1.75rem;display:flex;flex-direction:column;gap:0.9rem;">
  <div style="color:#fbbf24;font-size:0.9rem;letter-spacing:2px;">{stars}</div>
  <p style="font-size:0.92rem;line-height:1.72;color:{text};font-style:italic;">"{t.get('text','')}"</p>
  <div style="display:flex;align-items:center;gap:0.75rem;margin-top:auto;">
    <div style="width:38px;height:38px;border-radius:50%;background:linear-gradient(135deg,{brand},{accent});display:flex;align-items:center;justify-content:center;font-weight:700;color:{cta_txt_color};flex-shrink:0;">{t.get('name','A')[0]}</div>
    <div>
      <div style="font-weight:700;font-size:0.88rem;">{t.get('name','')}</div>
      <div style="font-size:0.76rem;color:{muted_col};">{t.get('role','')} · {t.get('company_size','')}</div>
    </div>
  </div>
</div>"""
        testimonials_html = f"""<section id="testimonials" style="padding:100px 0;">
  <div class="ctr">
    <div style="text-align:center;margin-bottom:3.5rem;">
      <span style="display:inline-block;font-size:0.72rem;letter-spacing:0.2em;text-transform:uppercase;color:{brand};font-weight:700;margin-bottom:0.75rem;padding:0.25rem 0.75rem;background:rgba({brand_r},{brand_g},{brand_b},0.1);border-radius:100px;">Testimonials</span>
      <h2 style="font-family:{hfont};font-size:clamp(2rem,4vw,3rem);font-weight:800;letter-spacing:-0.02em;">Loved by <em style="font-style:normal;color:{brand};">thousands</em></h2>
    </div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">{cards_t}</div>
  </div>
</section>"""

    # PRICING
    pricing_html = ""
    if s.get('show_pricing', True) and data.get('pricing'):
        price_cards = ""
        for plan in data.get('pricing', []):
            highlighted = plan.get('highlight', False)
            border_style = f"border-color:{brand};border-width:2px;" if highlighted else ""
            badge_p = f'<div style="position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:{brand};color:{cta_txt_color};padding:0.2rem 0.8rem;border-radius:100px;font-size:0.72rem;font-weight:700;white-space:nowrap;">{plan.get("badge","")}</div>' if plan.get('badge') else ''
            feature_list = " ".join([f'<li style="font-size:0.88rem;color:{muted_col};padding:0.35rem 0;border-bottom:1px solid {border_col};display:flex;align-items:center;gap:0.5rem;"><span style="color:{brand};">✓</span>{f}</li>' for f in plan.get('features', [])])
            price_cards += f"""<div style="background:{surface_color};border:1px solid {border_col};{border_style}border-radius:14px;padding:2rem;position:relative;{'box-shadow:0 8px 32px rgba(' + str(brand_r) + ',' + str(brand_g) + ',' + str(brand_b) + ',0.18);' if highlighted else ''}">
  {badge_p}
  <div style="font-size:0.72rem;letter-spacing:0.16em;text-transform:uppercase;color:{muted_col};font-weight:700;margin-bottom:0.6rem;">{plan.get('name','')}</div>
  <div style="display:flex;align-items:baseline;gap:0.2rem;margin-bottom:0.4rem;">
    <span style="font-family:{hfont};font-size:2.8rem;font-weight:800;color:{brand if highlighted else text};">{plan.get('price','')}</span>
    <span style="color:{muted_col};font-size:0.85rem;">{plan.get('period','')}</span>
  </div>
  <p style="font-size:0.85rem;color:{muted_col};margin-bottom:1.5rem;">{plan.get('desc','')}</p>
  <ul style="list-style:none;margin-bottom:1.75rem;">{feature_list}</ul>
  <a href="{cta_url}" style="display:block;text-align:center;padding:0.8rem;border-radius:8px;text-decoration:none;font-weight:700;font-size:0.9rem;{'background:' + brand + ';color:' + cta_txt_color + ';box-shadow:0 4px 14px rgba(' + str(brand_r) + ',' + str(brand_g) + ',' + str(brand_b) + ',0.35);' if highlighted else 'border:1.5px solid ' + border_col + ';color:' + text + ';'}">{plan.get('cta','Get Started')}</a>
</div>"""
        pricing_html = f"""<section id="pricing" style="padding:100px 0;background:{surface_color};">
  <div class="ctr">
    <div style="text-align:center;margin-bottom:4rem;">
      <span style="display:inline-block;font-size:0.72rem;letter-spacing:0.2em;text-transform:uppercase;color:{brand};font-weight:700;margin-bottom:0.75rem;padding:0.25rem 0.75rem;background:rgba({brand_r},{brand_g},{brand_b},0.1);border-radius:100px;">Pricing</span>
      <h2 style="font-family:{hfont};font-size:clamp(2rem,4vw,3rem);font-weight:800;letter-spacing:-0.02em;">Simple, <em style="font-style:normal;color:{brand};">transparent</em> pricing</h2>
    </div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">{price_cards}</div>
    <div style="text-align:center;margin-top:2rem;">
      <p style="font-size:0.88rem;color:{muted_col};">🔒 {data.get('guarantee','30-day money-back guarantee')}</p>
    </div>
  </div>
</section>"""

    # FAQ
    faq_html = ""
    if s.get('show_faq', True) and data.get('faq'):
        faq_items = ""
        for i, item in enumerate(data.get('faq', [])):
            faq_items += f"""<div style="border-bottom:1px solid {border_col};">
  <button onclick="var a=this.nextSibling;var i=this.querySelector('.fi');a.style.maxHeight=a.style.maxHeight?null:'200px';i.textContent=a.style.maxHeight?'−':'+';" style="width:100%;background:none;border:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;padding:1.2rem 0;font-family:{bfont};font-weight:600;font-size:0.97rem;color:{text};text-align:left;gap:1rem;">
    <span>{item.get('q','')}</span><span class="fi" style="font-size:1.2rem;color:{brand};flex-shrink:0;">+</span>
  </button>
  <div style="max-height:0;overflow:hidden;transition:max-height 0.4s ease;">
    <p style="padding-bottom:1.2rem;color:{muted_col};font-size:0.92rem;line-height:1.7;">{item.get('a','')}</p>
  </div>
</div>"""
        faq_html = f"""<section id="faq" style="padding:100px 0;">
  <div class="ctr">
    <div style="text-align:center;margin-bottom:3.5rem;">
      <span style="display:inline-block;font-size:0.72rem;letter-spacing:0.2em;text-transform:uppercase;color:{brand};font-weight:700;margin-bottom:0.75rem;padding:0.25rem 0.75rem;background:rgba({brand_r},{brand_g},{brand_b},0.1);border-radius:100px;">FAQ</span>
      <h2 style="font-family:{hfont};font-size:clamp(2rem,4vw,3rem);font-weight:800;letter-spacing:-0.02em;">Got <em style="font-style:normal;color:{brand};">questions?</em></h2>
    </div>
    <div style="max-width:700px;margin:0 auto;">{faq_items}</div>
  </div>
</section>"""

    # CTA BANNER
    cta_banner = ""
    if s.get('show_cta_banner', True):
        cta_banner = f"""<section style="padding:90px 0;background:linear-gradient(135deg,rgba({brand_r},{brand_g},{brand_b},0.14) 0%,rgba({acc_r},{acc_g},{acc_b},0.09) 100%);border-top:1px solid rgba({brand_r},{brand_g},{brand_b},0.22);border-bottom:1px solid rgba({brand_r},{brand_g},{brand_b},0.22);">
  <div class="ctr" style="display:flex;align-items:center;justify-content:space-between;gap:2rem;flex-wrap:wrap;">
    <div>
      <h2 style="font-family:{hfont};font-size:clamp(1.6rem,3.5vw,2.8rem);font-weight:800;letter-spacing:-0.01em;margin-bottom:0.4rem;">{data.get('headline','Ready to get started?')}</h2>
      <p style="color:{muted_col};font-size:1rem;">{data.get('footer_text','Join thousands of happy customers today.')}</p>
    </div>
    <div style="display:flex;gap:0.75rem;flex-shrink:0;flex-wrap:wrap;">
      <a href="{cta_url}" style="background:{brand};color:{cta_txt_color};padding:1rem 2.25rem;border-radius:8px;text-decoration:none;font-weight:700;font-size:0.95rem;box-shadow:0 4px 18px rgba({brand_r},{brand_g},{brand_b},0.38);">{data.get('cta_primary','Get Started')} →</a>
      <a href="#features" style="border:1.5px solid {border_col};color:{text};padding:1rem 2.25rem;border-radius:8px;text-decoration:none;font-weight:600;font-size:0.95rem;">{data.get('cta_secondary','Learn More')}</a>
    </div>
  </div>
</section>"""

    # FOOTER
    footer = f"""<footer style="padding:48px 0;border-top:1px solid {border_col};">
  <div class="ctr" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
    <div>
      <div style="font-family:{hfont};font-size:1.3rem;font-weight:800;color:{brand};margin-bottom:0.25rem;">{data.get('brand_name','Brand')}</div>
      <p style="font-size:0.8rem;color:{muted_col};">{data.get('tagline','')}</p>
    </div>
    <div style="display:flex;gap:2rem;flex-wrap:wrap;">
      <a href="#features" style="color:{muted_col};text-decoration:none;font-size:0.85rem;">Features</a>
      <a href="#pricing" style="color:{muted_col};text-decoration:none;font-size:0.85rem;">Pricing</a>
      <a href="#faq" style="color:{muted_col};text-decoration:none;font-size:0.85rem;">FAQ</a>
      <a href="{cta_url}" style="color:{brand};text-decoration:none;font-size:0.85rem;font-weight:700;">Get Started →</a>
    </div>
    <p style="font-size:0.78rem;color:{muted_col};">© {datetime.now().year} {data.get('brand_name','Brand')}. All rights reserved.</p>
  </div>
</footer>"""

    # SEO META TAGS
    seo = data.get('seo_meta', {})
    seo_tags = f"""
    <meta name="description" content="{seo.get('seo_description', data.get('subheadline',''))}">
    <meta name="keywords" content="{', '.join(seo.get('seo_keywords', data.get('seo_keywords',[])) or [])}">
    <meta property="og:title" content="{seo.get('og_title', data.get('headline',''))}">
    <meta property="og:description" content="{seo.get('og_description', data.get('subheadline',''))}">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{seo.get('twitter_title', data.get('headline',''))}">
    <meta name="twitter:description" content="{seo.get('twitter_description', data.get('subheadline',''))}">
    <link rel="canonical" href="https://yoursite.com/{seo.get('canonical_slug', 'landing')}">"""

    # FULL PAGE
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{seo.get('seo_title', data.get('headline','Landing Page'))} — {data.get('brand_name','Brand')}</title>
  {seo_tags}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{fimport}" rel="stylesheet">
  <style>
    *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}
    :root{{--brand:{brand};--accent:{accent};--bg:{bg};--text:{text};}}
    html{{scroll-behavior:smooth;}}
    body{{font-family:{bfont};{bg_css}color:{text};line-height:1.65;-webkit-font-smoothing:antialiased;}}
    {anim_css}
    .ctr{{max-width:1160px;margin:0 auto;padding:0 24px;}}
    a{{transition:all 0.2s ease;}}
    nav a{{color:{muted_col};text-decoration:none;font-size:0.9rem;font-weight:500;}}
    nav a:hover{{color:{text};}}
    @media(max-width:900px){{
      [style*="grid-template-columns:repeat(3"],[style*="grid-template-columns:repeat(4"]{{grid-template-columns:1fr 1fr !important;}}
      [style*="grid-template-columns:1fr 1fr"]:not(.keep-2col){{grid-template-columns:1fr !important;}}
    }}
    @media(max-width:640px){{
      .nav-links{{display:none !important;}}
      .nav-links.open{{display:flex !important;flex-direction:column;position:absolute;top:64px;left:0;right:0;background:{bg};padding:1rem;border-bottom:1px solid {border_col};z-index:999;}}
      .hamburger{{display:block !important;}}
      [style*="grid-template-columns"]{{grid-template-columns:1fr !important;}}
      .hero-split-inner{{grid-template-columns:1fr !important;}}
    }}
  </style>
</head>
<body>
{urgency_bar}
{nav}
{hero}
{logo_bar}
{stats_html}
{features_html}
{process_html}
{testimonials_html}
{pricing_html}
{faq_html}
{cta_banner}
{footer}
</body>
</html>"""


# ═══════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════
defs = {
    'page_data': None, 'description': '', 'tone': 'Professional',
    'industry': 'Technology', 'audience': 'B2B professionals',
    'lang': 'English', 'framework': 'SaaS / Startup',
    'brand_color': '#6c63ff', 'accent_color': '#ff6584',
    'bg_color': '#0d0d18', 'text_color': '#f0f0ff',
    'cta_url': '#signup', 'font_pair': 'Modern',
    'hero_layout': 'Centered', 'animation_style': 'Smooth',
    'bg_effect': 'Gradient Mesh',
    'nav_sticky': True, 'show_nav': True, 'show_stats': True,
    'show_testimonials': True, 'show_faq': True, 'show_cta_banner': True,
    'show_pricing': True, 'show_logos': True, 'show_urgency': True,
    'show_features': True, 'show_process': True,
    'gen_count': 0, 'ab_variant': None, 'seo_meta': None,
    'email_seq': None, 'social_copy': None, 'ad_copy': None,
    'history': [], 'active_history_idx': None,
    'custom_sections': [], 'custom_css': '',
    'last_gen_time': None,
}
for k, v in defs.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ═══════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="forge-header">
      <div class="forge-logo">PAGE<span>FORGE</span></div>
      <div class="forge-version">v2.0 · AI LANDING PAGE STUDIO</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("<div style='padding:1rem 1.1rem 0;'>", unsafe_allow_html=True)

        st.markdown('<span class="section-label">🔑 OpenAI API Key</span>', unsafe_allow_html=True)
        api_key = st.text_input("API Key", type="password", placeholder="sk-...", label_visibility="collapsed")

        col_m1, col_m2 = st.columns(2)
        with col_m1:
            model = st.selectbox("Model", ["gpt-4o","gpt-4o-mini","gpt-3.5-turbo"], label_visibility="visible")
        with col_m2:
            if api_key:
                st.markdown(f'<div style="background:rgba(54,211,126,0.1);border:1px solid rgba(54,211,126,0.3);border-radius:6px;padding:0.5rem;text-align:center;font-size:0.7rem;color:#36d37e;margin-top:1.55rem;font-family:\'Space Mono\',monospace;">✓ CONNECTED</div>', unsafe_allow_html=True)

        st.markdown('<hr class="forge-divider">', unsafe_allow_html=True)
        st.markdown('<span class="section-label">📊 Session Stats</span>', unsafe_allow_html=True)

        has = st.session_state.page_data is not None
        feat_n = len(st.session_state.page_data.get('features',[])) if has else 0
        wc = estimate_word_count(st.session_state.page_data) if has else 0

        st.markdown(f"""<div class="stat-row">
          <div class="stat-box"><div class="stat-num">{st.session_state.gen_count}</div><div class="stat-label">Gens</div></div>
          <div class="stat-box"><div class="stat-num">{len(st.session_state.history)}</div><div class="stat-label">History</div></div>
          <div class="stat-box"><div class="stat-num">{wc}</div><div class="stat-label">Words</div></div>
        </div>""", unsafe_allow_html=True)

        if has:
            scores, overall = score_copy(st.session_state.page_data)
            color = "#36d37e" if overall >= 75 else "#ffc44d" if overall >= 50 else "#ff3c5f"
            st.markdown(f"""<div style="background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:0.9rem;margin-top:0.5rem;">
              <div class="score-row"><span class="score-label">Copy Score</span><span class="score-val" style="color:{color};">{overall}/100</span></div>
              <div class="score-bar-wrap"><div class="score-bar" style="width:{overall}%;background:{color};"></div></div>
              <div style="margin-top:0.75rem;">""", unsafe_allow_html=True)
            for k, v in scores.items():
                c = "#36d37e" if v >= 75 else "#ffc44d" if v >= 50 else "#ff3c5f"
                st.markdown(f"""<div class="score-row" style="margin-bottom:0.3rem;">
                  <span class="score-label" style="font-size:0.55rem;">{k.replace('_',' ')}</span>
                  <span style="font-size:0.7rem;color:{c};font-family:'Space Mono',monospace;">{v}</span></div>
                  <div class="score-bar-wrap" style="margin-bottom:0.4rem;"><div class="score-bar" style="width:{v}%;background:{c};height:4px;"></div></div>""", unsafe_allow_html=True)
            st.markdown("</div></div>", unsafe_allow_html=True)

        st.markdown('<hr class="forge-divider">', unsafe_allow_html=True)

        # VERSION HISTORY
        if st.session_state.history:
            st.markdown('<span class="section-label">🕐 Version History</span>', unsafe_allow_html=True)
            for i, h in enumerate(reversed(st.session_state.history[-5:])):
                idx = len(st.session_state.history) - 1 - i
                ts = h.get('timestamp','')
                label = h.get('data',{}).get('headline','Version')[:28]
                if st.button(f"↩ {ts} — {label}...", key=f"hist_{idx}", use_container_width=True):
                    st.session_state.page_data = h['data']
                    st.rerun()

        st.markdown('<hr class="forge-divider">', unsafe_allow_html=True)

        # QUICK GUIDE
        st.markdown('<span class="section-label">📋 Quick Start</span>', unsafe_allow_html=True)
        guide = [("1","Describe your business below"),("2","Pick tone, industry, style"),("3","Hit ⚡ Generate"),("4","Edit in tabs, preview live"),("5","Export HTML or extras")]
        for num, txt in guide:
            st.markdown(f'<div style="display:flex;gap:0.6rem;margin-bottom:0.4rem;"><div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.4rem;color:rgba(255,60,95,0.3);line-height:1;min-width:1.2rem;">{num}</div><div style="font-size:0.75rem;color:#5a5f7a;padding-top:0.15rem;">{txt}</div></div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# MAIN AREA — HEADER
# ═══════════════════════════════════════════════════════
st.markdown("""
<div class="main-title">PAGE<span class="accent">FORGE</span> <span style="font-size:1.2rem;color:#2e3245;vertical-align:top;margin-top:1rem;display:inline-block;">v2</span></div>
<p style="font-family:'Space Mono',monospace;font-size:0.65rem;color:#5a5f7a;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:1.5rem;">
Generate · Customize · Score · Export · A/B Test · SEO · Social · Ads
</p>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# INPUT SECTION
# ═══════════════════════════════════════════════════════
with st.expander("⚙️  Setup — Business Description & Generation Settings", expanded=not bool(st.session_state.page_data)):
    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.markdown('<span class="section-label">💡 Business Description</span>', unsafe_allow_html=True)

        # Prompt starters
        st.markdown("""<p style="font-size:0.72rem;color:#5a5f7a;margin-bottom:0.4rem;">Quick starters (click to use):</p>""", unsafe_allow_html=True)
        starters = [
            "AI-powered analytics platform for e-commerce brands",
            "Freelance project management tool for creative agencies",
            "Health coaching app with AI meal planning",
            "B2B SaaS for automated invoice processing",
            "Online course platform for professional development",
        ]
        starter_pills = "".join([f'<span class="prompt-pill" onclick="navigator.clipboard.writeText(\'{s}\')">{s}</span>' for s in starters])
        st.markdown(f'<div>{starter_pills}</div>', unsafe_allow_html=True)

        st.session_state.description = st.text_area(
            "Description", value=st.session_state.description, height=110,
            placeholder="Describe your product or business. The more detail you provide, the better the output.\n\nE.g: A SaaS tool for e-commerce teams that automates return management. Target: DTC brands doing $1M-$50M ARR. Unique value: cuts return processing time by 80% and increases exchange rates.",
            label_visibility="collapsed"
        )

    with col_b:
        col_t, col_i = st.columns(2)
        with col_t:
            tones = ["Professional","Bold & Direct","Playful","Luxury","Minimalist","Technical","Urgent","Friendly","Inspirational","Witty"]
            st.session_state.tone = st.selectbox("Tone", tones)
        with col_i:
            industries = ["Technology","SaaS","E-commerce","Healthcare","Finance","Education","Creative Agency","Real Estate","Food & Bev","Legal","Other"]
            st.session_state.industry = st.selectbox("Industry", industries)

        st.session_state.audience = st.text_input("Target Audience", value=st.session_state.audience)

        col_l, col_f = st.columns(2)
        with col_l:
            langs = ["English","Spanish","French","German","Portuguese","Italian","Dutch","Japanese","Chinese"]
            st.session_state.lang = st.selectbox("Language", langs)
        with col_f:
            frameworks = ["SaaS / Startup","Agency / Studio","E-commerce","Healthcare","Fintech","Education","Enterprise","Non-profit"]
            st.session_state.framework = st.selectbox("Page Vibe", frameworks)

    st.markdown('<div class="tip-block">💡 <strong>Pro tip:</strong> Include your pricing range, main competitor advantage, key pain points, and 1-2 specific customer outcomes for dramatically better AI output.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# GENERATE BUTTON ROW
# ═══════════════════════════════════════════════════════
col_g1, col_g2, col_g3, col_g4 = st.columns([2, 1, 1, 1])

with col_g1:
    gen = st.button("⚡ Generate Full Landing Page", use_container_width=True)
with col_g2:
    regen = st.button("🔄 Regenerate", use_container_width=True, disabled=not bool(st.session_state.page_data))
with col_g3:
    rand_tone = st.button("🎲 Random Tone", use_container_width=True)
with col_g4:
    clear = st.button("🗑️ Clear All", use_container_width=True)

if rand_tone:
    tones_list = ["Professional","Bold & Direct","Playful","Luxury","Minimalist","Technical","Urgent","Friendly","Inspirational","Witty"]
    st.session_state.tone = random.choice(tones_list)
    st.rerun()

if clear:
    st.session_state.page_data = None
    st.session_state.ab_variant = None
    st.session_state.seo_meta = None
    st.session_state.email_seq = None
    st.session_state.social_copy = None
    st.session_state.ad_copy = None
    st.rerun()

def do_generate(api_key, model):
    if not api_key:
        st.error("❌ OpenAI API key required in the sidebar.")
        return
    if not st.session_state.description.strip():
        st.error("❌ Please enter a business description.")
        return

    prog = st.progress(0)
    status = st.empty()
    status.info("🤖 AI is crafting your landing page content...")
    prog.progress(10)

    data = generate_full_page(
        st.session_state.description, st.session_state.tone,
        st.session_state.industry, st.session_state.audience,
        st.session_state.lang, st.session_state.framework,
        api_key, model
    )
    prog.progress(85)

    if data:
        # Save to history
        st.session_state.history.append({
            'data': st.session_state.page_data,
            'timestamp': datetime.now().strftime('%H:%M'),
        })
        if st.session_state.page_data:
            st.session_state.history = [h for h in st.session_state.history if h['data'] is not None]

        st.session_state.page_data = data
        st.session_state.gen_count += 1
        st.session_state.last_gen_time = datetime.now().strftime('%H:%M:%S')
        # Clear downstream extras
        st.session_state.ab_variant = None
        st.session_state.seo_meta = None
        st.session_state.email_seq = None
        st.session_state.social_copy = None
        st.session_state.ad_copy = None

        prog.progress(100)
        status.success(f"✅ Done! {len(data.get('features',[]))} features · {len(data.get('testimonials',[]))} testimonials · {len(data.get('faq',[]))} FAQs · {len(data.get('pricing',[]))} pricing tiers")
    else:
        prog.empty()
        status.error("❌ Generation failed. Check API key and try again.")

if gen or regen:
    do_generate(api_key, model)
    st.rerun()


# ═══════════════════════════════════════════════════════
# MAIN EDITOR (only when data exists)
# ═══════════════════════════════════════════════════════
if st.session_state.page_data:
    data = st.session_state.page_data

    st.markdown("---")

    # ── MASTER TABS ──
    tabs = st.tabs([
        "✏️ Copy", "🎨 Design", "🧩 Sections",
        "🔬 A/B Test", "🔍 SEO", "📧 Email", "📱 Social", "📢 Ads",
        "👁️ Preview", "💻 Code", "📦 Export"
    ])

    # ────────────────────────────────────────────
    # TAB 1: COPY EDITOR
    # ────────────────────────────────────────────
    with tabs[0]:
        st.markdown('<div class="section-chip">✏️ COPY EDITOR</div>', unsafe_allow_html=True)

        # Hero copy
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            data['brand_name'] = st.text_input("🏷️ Brand Name", value=data.get('brand_name',''))
            data['tagline']     = st.text_input("✨ Tagline", value=data.get('tagline',''))
            data['headline']    = st.text_input("🔥 Headline", value=data.get('headline',''))
            data['subheadline'] = st.text_input("📌 Subheadline", value=data.get('subheadline',''))
        with col_h2:
            data['cta_primary']   = st.text_input("🔘 Primary CTA", value=data.get('cta_primary',''))
            data['cta_secondary'] = st.text_input("🔲 Secondary CTA", value=data.get('cta_secondary',''))
            st.session_state.cta_url = st.text_input("🔗 CTA URL", value=st.session_state.cta_url)
            data['email_placeholder'] = st.text_input("📧 Email Placeholder", value=data.get('email_placeholder',''))

        data['hero_body']    = st.text_area("📝 Hero Body", value=data.get('hero_body',''), height=100)
        data['social_proof'] = st.text_input("🏆 Social Proof Badge", value=data.get('social_proof',''))
        data['urgency_text'] = st.text_input("⏰ Urgency Bar Text (leave blank to hide)", value=data.get('urgency_text',''))
        data['guarantee']    = st.text_input("🔒 Guarantee Text", value=data.get('guarantee',''))
        data['footer_text']  = st.text_input("👇 Footer Tagline", value=data.get('footer_text',''))

        st.markdown("---")
        col_regen_h, col_regen_cta = st.columns(2)
        with col_regen_h:
            if st.button("🎲 Regen Headlines (AI)", use_container_width=True):
                if api_key:
                    with st.spinner("Generating..."):
                        res = regenerate_section("headline", f"{data.get('brand_name')} — {st.session_state.description}", api_key, model, st.session_state.tone)
                        if res and res.get('options'):
                            for i, opt in enumerate(res['options'][:5]):
                                st.markdown(f'<div style="background:var(--surface2);border:1px solid var(--border);border-radius:6px;padding:0.6rem 0.9rem;margin-bottom:0.4rem;font-size:0.9rem;">{i+1}. {opt}</div>', unsafe_allow_html=True)
        with col_regen_cta:
            if st.button("🎲 Regen CTAs (AI)", use_container_width=True):
                if api_key:
                    with st.spinner("Generating..."):
                        res = regenerate_section("cta", f"{data.get('brand_name')} — {st.session_state.description}", api_key, model, st.session_state.tone)
                        if res and res.get('options'):
                            for opt in res['options'][:6]:
                                st.markdown(f'<div style="background:var(--surface2);border:1px solid var(--border);border-radius:6px;padding:0.4rem 0.75rem;margin-bottom:0.3rem;font-size:0.85rem;">{opt}</div>', unsafe_allow_html=True)

        # FEATURES
        st.markdown("---")
        st.markdown('<div class="section-chip blue">⚡ FEATURES</div>', unsafe_allow_html=True)

        col_regen_f, col_add_f = st.columns(2)
        with col_regen_f:
            if st.button("🎲 Regen Features (AI)", use_container_width=True):
                if api_key:
                    with st.spinner("Regenerating..."):
                        res = regenerate_section("features", st.session_state.description, api_key, model)
                        if res and res.get('features'):
                            data['features'] = res['features']
                            st.rerun()
        with col_add_f:
            if st.button("➕ Add Feature", use_container_width=True):
                data['features'].append({"icon":"⭐","title":"New Feature","desc":"Describe the benefit of this feature in 20-30 words."})
                st.rerun()

        feats = data.get('features', [])
        cols_f = st.columns(2)
        new_feats = []
        for i, f in enumerate(feats):
            with cols_f[i % 2]:
                with st.expander(f"{f.get('icon','⚡')} {f.get('title','Feature')}", expanded=False):
                    c1, c2 = st.columns([1, 5])
                    with c1: icon = st.text_input("Icon", value=f.get('icon','⚡'), key=f"ficon_{i}")
                    with c2: title = st.text_input("Title", value=f.get('title',''), key=f"ftit_{i}")
                    desc = st.text_area("Desc", value=f.get('desc',''), key=f"fdesc_{i}", height=70)
                    col_del_f, _ = st.columns([1, 3])
                    with col_del_f:
                        if st.button("🗑️ Remove", key=f"fdel_{i}"):
                            feats.pop(i); data['features'] = feats; st.rerun()
                    new_feats.append({"icon":icon,"title":title,"desc":desc})
        if new_feats:
            data['features'] = new_feats

        # TESTIMONIALS
        st.markdown("---")
        st.markdown('<div class="section-chip gold">💬 TESTIMONIALS</div>', unsafe_allow_html=True)

        col_regen_t, col_add_t = st.columns(2)
        with col_regen_t:
            if st.button("🎲 Regen Testimonials (AI)", use_container_width=True):
                if api_key:
                    with st.spinner():
                        res = regenerate_section("testimonials", st.session_state.description, api_key, model)
                        if res and res.get('testimonials'):
                            data['testimonials'] = res['testimonials']; st.rerun()
        with col_add_t:
            if st.button("➕ Add Testimonial", use_container_width=True):
                data.setdefault('testimonials', []).append({"name":"New Person","role":"Title, Company","text":"Testimonial text here.","rating":5,"company_size":"Startup"})
                st.rerun()

        for i, t in enumerate(data.get('testimonials',[])):
            with st.expander(f"💬 {t.get('name','Testimonial')} — {t.get('role','')}", expanded=False):
                c1,c2,c3 = st.columns(3)
                with c1: t['name'] = st.text_input("Name", value=t.get('name',''), key=f"tname_{i}")
                with c2: t['role'] = st.text_input("Role", value=t.get('role',''), key=f"trole_{i}")
                with c3: t['rating'] = st.slider("⭐", 1, 5, t.get('rating',5), key=f"trat_{i}")
                t['text'] = st.text_area("Text", value=t.get('text',''), key=f"ttxt_{i}", height=80)
                t['company_size'] = st.text_input("Company Size", value=t.get('company_size',''), key=f"tcs_{i}")

        # STATS
        st.markdown("---")
        st.markdown('<div class="section-chip teal">📊 STATS</div>', unsafe_allow_html=True)

        col_regen_s, col_add_s = st.columns(2)
        with col_regen_s:
            if st.button("🎲 Regen Stats (AI)", use_container_width=True):
                if api_key:
                    with st.spinner():
                        res = regenerate_section("stats", st.session_state.description, api_key, model)
                        if res and res.get('stats'):
                            data['stats'] = res['stats']; st.rerun()
        with col_add_s:
            if st.button("➕ Add Stat", use_container_width=True):
                data.setdefault('stats', []).append({"num":"99%","label":"New Stat","icon":"⭐"})
                st.rerun()

        stat_cols = st.columns(4)
        for i, st_item in enumerate(data.get('stats',[])):
            with stat_cols[i % 4]:
                c1,c2 = st.columns([1,2])
                with c1: st_item['icon'] = st.text_input("I", value=st_item.get('icon','⭐'), key=f"sico_{i}")
                with c2: st_item['num'] = st.text_input("Num", value=st_item.get('num',''), key=f"snum_{i}")
                st_item['label'] = st.text_input("Label", value=st_item.get('label',''), key=f"slbl_{i}")

        # PRICING
        st.markdown("---")
        st.markdown('<div class="section-chip purple">💳 PRICING</div>', unsafe_allow_html=True)

        col_regen_p, col_add_p = st.columns(2)
        with col_regen_p:
            if st.button("🎲 Regen Pricing (AI)", use_container_width=True):
                if api_key:
                    with st.spinner():
                        res = regenerate_section("pricing", st.session_state.description, api_key, model)
                        if res and res.get('pricing'):
                            data['pricing'] = res['pricing']; st.rerun()
        with col_add_p:
            if st.button("➕ Add Tier", use_container_width=True):
                data.setdefault('pricing', []).append({"name":"New Plan","price":"$99","period":"/mo","desc":"Description","highlight":False,"cta":"Get Started","features":["Feature A","Feature B"]})
                st.rerun()

        for i, plan in enumerate(data.get('pricing',[])):
            with st.expander(f"💳 {plan.get('name','')} — {plan.get('price','')}", expanded=False):
                c1,c2,c3,c4 = st.columns(4)
                with c1: plan['name'] = st.text_input("Name", value=plan.get('name',''), key=f"pname_{i}")
                with c2: plan['price'] = st.text_input("Price", value=plan.get('price',''), key=f"pprice_{i}")
                with c3: plan['period'] = st.text_input("Period", value=plan.get('period',''), key=f"pper_{i}")
                with c4: plan['highlight'] = st.checkbox("Featured", value=plan.get('highlight',False), key=f"phil_{i}")
                plan['desc'] = st.text_input("Description", value=plan.get('desc',''), key=f"pdesc_{i}")
                plan['cta'] = st.text_input("CTA Button", value=plan.get('cta',''), key=f"pcta_{i}")
                plan['badge'] = st.text_input("Badge (optional)", value=plan.get('badge',''), key=f"pbadge_{i}")
                feats_str = "\n".join(plan.get('features',[]))
                new_feats_str = st.text_area("Features (one per line)", value=feats_str, key=f"pfeats_{i}", height=100)
                plan['features'] = [f.strip() for f in new_feats_str.split('\n') if f.strip()]

        # PROCESS
        st.markdown("---")
        st.markdown('<div class="section-chip success">🔢 PROCESS STEPS</div>', unsafe_allow_html=True)

        col_regen_pr, col_add_pr = st.columns(2)
        with col_regen_pr:
            if st.button("🎲 Regen Process (AI)", use_container_width=True):
                if api_key:
                    with st.spinner():
                        res = regenerate_section("process", st.session_state.description, api_key, model)
                        if res and res.get('steps'):
                            data['process_steps'] = res['steps']; st.rerun()
        with col_add_pr:
            if st.button("➕ Add Step", use_container_width=True):
                steps = data.get('process_steps', [])
                n = len(steps) + 1
                steps.append({"step":f"0{n}","title":"New Step","desc":"Describe what happens in this step."})
                data['process_steps'] = steps; st.rerun()

        for i, step in enumerate(data.get('process_steps',[])):
            with st.expander(f"🔢 {step.get('step','0'+str(i+1))} — {step.get('title','')}", expanded=False):
                c1,c2 = st.columns([1,4])
                with c1: step['step'] = st.text_input("Step #", value=step.get('step',''), key=f"prstep_{i}")
                with c2: step['title'] = st.text_input("Title", value=step.get('title',''), key=f"prtit_{i}")
                step['desc'] = st.text_area("Description", value=step.get('desc',''), key=f"prdesc_{i}", height=70)

        # FAQ
        st.markdown("---")
        st.markdown('<div class="section-chip">❓ FAQ</div>', unsafe_allow_html=True)

        col_regen_fq, col_add_fq = st.columns(2)
        with col_regen_fq:
            if st.button("🎲 Regen FAQ (AI)", use_container_width=True):
                if api_key:
                    with st.spinner():
                        res = regenerate_section("faq", st.session_state.description, api_key, model)
                        if res and res.get('faq'):
                            data['faq'] = res['faq']; st.rerun()
        with col_add_fq:
            if st.button("➕ Add FAQ Item", use_container_width=True):
                data.setdefault('faq',[]).append({"q":"New question?","a":"Answer here."})
                st.rerun()

        for i, item in enumerate(data.get('faq',[])):
            with st.expander(f"❓ {item.get('q','FAQ')[:50]}...", expanded=False):
                item['q'] = st.text_input("Question", value=item.get('q',''), key=f"fqq_{i}")
                item['a'] = st.text_area("Answer", value=item.get('a',''), key=f"fqa_{i}", height=80)
                if st.button("🗑️ Remove", key=f"fqdel_{i}"):
                    data['faq'].pop(i); st.rerun()

        # LOGOS
        st.markdown("---")
        st.markdown('<span class="section-label">🏢 Trust Logo Bar</span>', unsafe_allow_html=True)
        logos_str = ", ".join(data.get('logos',[]))
        new_logos = st.text_input("Company Names (comma-separated)", value=logos_str)
        data['logos'] = [l.strip() for l in new_logos.split(',') if l.strip()]

        # NAV LINKS
        nav_str = ", ".join(data.get('nav_links',[]))
        new_nav = st.text_input("Nav Links (comma-separated)", value=nav_str)
        data['nav_links'] = [l.strip() for l in new_nav.split(',') if l.strip()]

    # ────────────────────────────────────────────
    # TAB 2: DESIGN
    # ────────────────────────────────────────────
    with tabs[1]:
        st.markdown('<div class="section-chip blue">🎨 DESIGN SYSTEM</div>', unsafe_allow_html=True)

        col_d1, col_d2, col_d3 = st.columns(3)

        with col_d1:
            st.markdown("**Colors**")
            st.session_state.brand_color  = st.color_picker("Brand Color",  st.session_state.brand_color)
            st.session_state.accent_color = st.color_picker("Accent Color", st.session_state.accent_color)
            st.session_state.bg_color     = st.color_picker("Background",   st.session_state.bg_color)
            st.session_state.text_color   = st.color_picker("Text Color",   st.session_state.text_color)

            st.markdown("**Quick Themes**")
            themes = {
                "🌑 Dark":    ("#6c63ff","#ff6584","#0d0d18","#f0f0ff"),
                "☀️ Light":   ("#5c4ee5","#ff4d8d","#fafafa","#1a1a2e"),
                "🌿 Forest":  ("#2d8a5e","#ff7043","#0f1f17","#e8f5e9"),
                "🥃 Bourbon": ("#c9a96e","#ff6b6b","#0f1117","#f0ede8"),
                "🌊 Ocean":   ("#0891b2","#f59e0b","#0c1523","#e0f2fe"),
                "🔥 Fire":    ("#ef4444","#f97316","#1c0a00","#fef3e2"),
                "💜 Purple":  ("#9333ea","#ec4899","#0f0a1a","#fdf4ff"),
                "🏁 Mono":    ("#f5f5f5","#888888","#111111","#f5f5f5"),
                "🌸 Sakura":  ("#f06292","#ffb74d","#1a0a10","#fce4ec"),
                "🌌 Galaxy":  ("#7c4dff","#40c4ff","#030311","#e8eaff"),
                "🍋 Citrus":  ("#f59e0b","#10b981","#0f1a0a","#fffde7"),
                "🖤 Charcoal":("#e2e8f0","#94a3b8","#1e293b","#f8fafc"),
            }
            t_cols = st.columns(3)
            for i, (name, colors) in enumerate(themes.items()):
                with t_cols[i % 3]:
                    if st.button(name, key=f"theme_{name}"):
                        st.session_state.brand_color = colors[0]
                        st.session_state.accent_color = colors[1]
                        st.session_state.bg_color = colors[2]
                        st.session_state.text_color = colors[3]
                        st.rerun()

        with col_d2:
            st.markdown("**Typography**")
            fonts = ["Modern","Editorial","Technical","Elegant","Bold","Futuristic","Humanist","Retro"]
            st.session_state.font_pair = st.radio("Font Style", fonts,
                index=fonts.index(st.session_state.font_pair) if st.session_state.font_pair in fonts else 0)

            st.markdown("**Hero Layout**")
            layouts = ["Centered","Split","Minimal","Magazine","Video"]
            st.session_state.hero_layout = st.radio("Layout", layouts,
                index=layouts.index(st.session_state.hero_layout) if st.session_state.hero_layout in layouts else 0)

        with col_d3:
            st.markdown("**Animation**")
            anims = ["Smooth","Dramatic","Typewriter","None"]
            st.session_state.animation_style = st.radio("Animation", anims,
                index=anims.index(st.session_state.animation_style) if st.session_state.animation_style in anims else 0)

            st.markdown("**Background Effect**")
            bgs = ["Gradient Mesh","Dots","Grid","Lines","Diagonal","Gradient","Solid"]
            st.session_state.bg_effect = st.radio("Background", bgs,
                index=bgs.index(st.session_state.bg_effect) if st.session_state.bg_effect in bgs else 0)

            st.markdown("**Custom CSS**")
            st.session_state.custom_css = st.text_area("Additional CSS", value=st.session_state.custom_css, height=100, placeholder="/* Your custom CSS here */")

    # ────────────────────────────────────────────
    # TAB 3: SECTIONS
    # ────────────────────────────────────────────
    with tabs[2]:
        st.markdown('<div class="section-chip teal">🧩 SECTION CONTROL</div>', unsafe_allow_html=True)

        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.markdown("**Navigation & Hero**")
            st.session_state.show_nav         = st.checkbox("🧭 Navigation Bar",    value=st.session_state.show_nav)
            st.session_state.nav_sticky       = st.checkbox("📌 Sticky Nav",         value=st.session_state.nav_sticky)
            st.session_state.show_urgency     = st.checkbox("⏰ Urgency Banner",     value=st.session_state.show_urgency)
            st.session_state.show_logos       = st.checkbox("🏢 Logo Bar",           value=st.session_state.show_logos)
        with col_s2:
            st.markdown("**Content Sections**")
            st.session_state.show_stats       = st.checkbox("📊 Stats Section",      value=st.session_state.show_stats)
            st.session_state.show_features    = st.checkbox("⚡ Features Grid",      value=st.session_state.show_features)
            st.session_state.show_process     = st.checkbox("🔢 Process Steps",      value=st.session_state.show_process)
            st.session_state.show_testimonials= st.checkbox("💬 Testimonials",       value=st.session_state.show_testimonials)
        with col_s3:
            st.markdown("**Conversion Sections**")
            st.session_state.show_pricing     = st.checkbox("💳 Pricing Table",      value=st.session_state.show_pricing)
            st.session_state.show_faq         = st.checkbox("❓ FAQ Section",        value=st.session_state.show_faq)
            st.session_state.show_cta_banner  = st.checkbox("🎯 CTA Banner",         value=st.session_state.show_cta_banner)

        st.markdown("---")
        st.markdown('<div class="info-block">💡 <strong>Section order is fixed</strong> for optimal conversion flow: Nav → Hero → Logos → Stats → Features → Process → Testimonials → Pricing → FAQ → CTA → Footer</div>', unsafe_allow_html=True)

    # ────────────────────────────────────────────
    # TAB 4: A/B TEST
    # ────────────────────────────────────────────
    with tabs[3]:
        st.markdown('<div class="section-chip">🔬 A/B TEST VARIANT GENERATOR</div>', unsafe_allow_html=True)

        st.markdown("""<div class="info-block">
        Generate an AI-powered A/B test variant with a different messaging angle — different emotional hook,
        different value prop framing, different CTA. Use this to test which approach resonates more with your audience.
        </div>""", unsafe_allow_html=True)

        if st.button("🧪 Generate A/B Variant (AI)", use_container_width=True):
            if api_key:
                with st.spinner("Creating variant..."):
                    variant = generate_ab_variant(data, api_key, model)
                    if variant:
                        st.session_state.ab_variant = variant
                        st.rerun()

        if st.session_state.ab_variant:
            v = st.session_state.ab_variant
            st.markdown("---")
            st.markdown('<span class="section-label">🅰 ORIGINAL</span>', unsafe_allow_html=True)
            col_a_v, col_b_v = st.columns(2)
            with col_a_v:
                st.markdown(f"**Headline:** {data.get('headline','')}")
                st.markdown(f"**CTA:** {data.get('cta_primary','')}")
                st.text_area("Hero (A)", value=data.get('hero_body',''), height=100, disabled=True, key="ab_a_hero")

            st.markdown('<span class="section-label">🅱 VARIANT</span>', unsafe_allow_html=True)
            with col_b_v:
                st.markdown(f"**Headline:** {v.get('headline','')}")
                st.markdown(f"**CTA:** {v.get('cta_primary','')}")
                st.text_area("Hero (B)", value=v.get('hero_body',''), height=100, disabled=True, key="ab_b_hero")

            st.markdown(f'<div class="tip-block">🔬 <strong>Rationale:</strong> {v.get("variant_rationale","")}</div>', unsafe_allow_html=True)

            col_ab1, col_ab2 = st.columns(2)
            with col_ab1:
                if st.button("✅ Use Variant B (replace current)", use_container_width=True):
                    data['headline']    = v.get('headline', data['headline'])
                    data['subheadline'] = v.get('subheadline', data['subheadline'])
                    data['hero_body']   = v.get('hero_body', data['hero_body'])
                    data['cta_primary'] = v.get('cta_primary', data['cta_primary'])
                    st.session_state.ab_variant = None
                    st.success("✅ Variant B applied!")
                    st.rerun()
            with col_ab2:
                if st.button("🗑️ Discard Variant", use_container_width=True):
                    st.session_state.ab_variant = None
                    st.rerun()

            # Export both as downloadable JSON
            ab_export = {"variant_a": {k: data.get(k) for k in ['headline','subheadline','hero_body','cta_primary']}, "variant_b": v, "rationale": v.get('variant_rationale')}
            st.download_button("⬇️ Export A/B Data JSON", data=json.dumps(ab_export, indent=2), file_name="ab_variants.json", mime="application/json", use_container_width=True)

    # ────────────────────────────────────────────
    # TAB 5: SEO
    # ────────────────────────────────────────────
    with tabs[4]:
        st.markdown('<div class="section-chip blue">🔍 SEO OPTIMIZER</div>', unsafe_allow_html=True)

        col_seo1, col_seo2 = st.columns([2, 1])
        with col_seo1:
            if st.button("🔍 Generate Full SEO Meta (AI)", use_container_width=True):
                if api_key:
                    with st.spinner("Analyzing and generating SEO..."):
                        seo = generate_seo_meta(data, api_key, model)
                        if seo:
                            st.session_state.seo_meta = seo
                            data['seo_meta'] = seo
                            st.rerun()
        with col_seo2:
            if st.session_state.seo_meta:
                st.success("✅ SEO meta generated")

        if st.session_state.seo_meta:
            seo = st.session_state.seo_meta
            st.markdown("---")

            # SEO Analysis
            title_len = len(seo.get('seo_title',''))
            desc_len  = len(seo.get('seo_description',''))
            t_color   = "#36d37e" if 40 <= title_len <= 60 else "#ffc44d"
            d_color   = "#36d37e" if 130 <= desc_len <= 155 else "#ffc44d"

            col_t_meta, col_d_meta = st.columns(2)
            with col_t_meta:
                st.markdown(f'<span class="section-label">PAGE TITLE <span style="color:{t_color};">({title_len}/60 chars)</span></span>', unsafe_allow_html=True)
                seo['seo_title'] = st.text_input("SEO Title", value=seo.get('seo_title',''), label_visibility="collapsed")
            with col_d_meta:
                st.markdown(f'<span class="section-label">META DESCRIPTION <span style="color:{d_color};">({desc_len}/155 chars)</span></span>', unsafe_allow_html=True)
                seo['seo_description'] = st.text_area("Meta Desc", value=seo.get('seo_description',''), height=70, label_visibility="collapsed")

            col_og1, col_og2 = st.columns(2)
            with col_og1:
                seo['og_title'] = st.text_input("OG Title", value=seo.get('og_title',''))
                seo['og_description'] = st.text_area("OG Description", value=seo.get('og_description',''), height=70)
            with col_og2:
                seo['twitter_title'] = st.text_input("Twitter Title", value=seo.get('twitter_title',''))
                seo['twitter_description'] = st.text_area("Twitter Description", value=seo.get('twitter_description',''), height=70)

            seo['canonical_slug'] = st.text_input("Canonical Slug", value=seo.get('canonical_slug',''))

            kws = seo.get('seo_keywords', [])
            kw_str = ", ".join(kws)
            new_kw = st.text_input("Keywords (comma-separated)", value=kw_str)
            seo['seo_keywords'] = [k.strip() for k in new_kw.split(',') if k.strip()]

            # Keyword pills
            st.markdown("**Keywords:**")
            pills_html = " ".join([f'<span class="prompt-pill">{k}</span>' for k in seo.get('seo_keywords',[])])
            st.markdown(f'<div>{pills_html}</div>', unsafe_allow_html=True)

            # Export SEO as JSON
            st.download_button("⬇️ Export SEO Meta JSON", data=json.dumps(seo, indent=2), file_name="seo_meta.json", mime="application/json", use_container_width=True)

            data['seo_meta'] = seo

        else:
            st.markdown('<div class="warn-block">👆 Click "Generate SEO Meta" above to get AI-powered title tags, meta descriptions, Open Graph tags, Twitter cards, canonical URLs, and keywords.</div>', unsafe_allow_html=True)

            # Manual fallback
            st.markdown("**Or fill in manually:**")
            c1, c2 = st.columns(2)
            with c1:
                data['seo_title'] = st.text_input("SEO Title", value=data.get('seo_title', data.get('headline','')))
                data['seo_description'] = st.text_area("Meta Description", value=data.get('seo_description', data.get('subheadline','')), height=80)
            with c2:
                kws_manual = ", ".join(data.get('seo_keywords', []))
                new_kws = st.text_input("Keywords", value=kws_manual)
                data['seo_keywords'] = [k.strip() for k in new_kws.split(',') if k.strip()]

    # ────────────────────────────────────────────
    # TAB 6: EMAIL SEQUENCE
    # ────────────────────────────────────────────
    with tabs[5]:
        st.markdown('<div class="section-chip gold">📧 EMAIL SEQUENCE GENERATOR</div>', unsafe_allow_html=True)

        st.markdown("""<div class="info-block">
        Generate a 3-email welcome sequence for new signups. Perfect for nurturing leads after they convert on your landing page.
        </div>""", unsafe_allow_html=True)

        if st.button("📧 Generate Email Sequence (AI)", use_container_width=True):
            if api_key:
                with st.spinner("Writing your email sequence..."):
                    eq = generate_email_sequence(data, api_key, model)
                    if eq:
                        st.session_state.email_seq = eq
                        st.rerun()

        if st.session_state.email_seq:
            emails = st.session_state.email_seq.get('emails', [])
            day_labels = ["Day 0 — Welcome", "Day 3 — Follow-up", "Day 7 — Value Drop"]

            for i, email in enumerate(emails):
                label = day_labels[i] if i < len(day_labels) else f"Email {i+1}"
                with st.expander(f"📧 {label} — {email.get('subject','')}", expanded=(i==0)):
                    col_sub, col_pre = st.columns(2)
                    with col_sub:
                        email['subject'] = st.text_input("Subject Line", value=email.get('subject',''), key=f"esubj_{i}")
                    with col_pre:
                        email['preview'] = st.text_input("Preview Text", value=email.get('preview',''), key=f"eprev_{i}")
                    email['body'] = st.text_area("Email Body", value=email.get('body',''), key=f"ebody_{i}", height=150)
                    email['cta']  = st.text_input("CTA Button", value=email.get('cta',''), key=f"ecta_{i}")

            # Export
            col_exp_e1, col_exp_e2 = st.columns(2)
            with col_exp_e1:
                st.download_button("⬇️ Export Emails JSON", data=json.dumps(st.session_state.email_seq, indent=2), file_name="email_sequence.json", mime="application/json", use_container_width=True)
            with col_exp_e2:
                # Format as plain text
                email_txt = "\n\n".join([f"{'='*60}\n{day_labels[i] if i < len(day_labels) else 'Email '+str(i+1)}\n{'='*60}\nSUBJECT: {e.get('subject','')}\nPREVIEW: {e.get('preview','')}\n\n{e.get('body','')}\n\nCTA: {e.get('cta','')}" for i, e in enumerate(emails)])
                st.download_button("⬇️ Export Emails TXT", data=email_txt, file_name="email_sequence.txt", mime="text/plain", use_container_width=True)

    # ────────────────────────────────────────────
    # TAB 7: SOCIAL COPY
    # ────────────────────────────────────────────
    with tabs[6]:
        st.markdown('<div class="section-chip teal">📱 SOCIAL MEDIA COPY</div>', unsafe_allow_html=True)

        if st.button("📱 Generate Social Copy (AI)", use_container_width=True):
            if api_key:
                with st.spinner("Writing social posts..."):
                    sc = generate_social_copy(data, api_key, model)
                    if sc:
                        st.session_state.social_copy = sc
                        st.rerun()

        if st.session_state.social_copy:
            sc = st.session_state.social_copy

            st.markdown("---")
            st.markdown("**🐦 Twitter/X Tweets**")
            tweets = sc.get('twitter', [])
            for i, tweet in enumerate(tweets):
                col_tw, col_copy = st.columns([5, 1])
                with col_tw:
                    sc['twitter'][i] = st.text_area(f"Tweet {i+1} ({len(tweet)}/280)", value=tweet, key=f"tw_{i}", height=80)
                with col_copy:
                    st.code(tweet[:50]+"...", language=None)

            st.markdown("---")
            st.markdown("**💼 LinkedIn Post**")
            sc['linkedin'] = st.text_area("LinkedIn", value=sc.get('linkedin',''), height=180)

            st.markdown("---")
            st.markdown("**📸 Instagram Caption**")
            sc['instagram_caption'] = st.text_area("Instagram", value=sc.get('instagram_caption',''), height=120)

            st.markdown("---")
            col_ph, col_red = st.columns(2)
            with col_ph:
                st.markdown("**🚀 Product Hunt Tagline**")
                sc['product_hunt_tagline'] = st.text_input("Product Hunt", value=sc.get('product_hunt_tagline',''))
            with col_red:
                st.markdown("**🔴 Reddit Title**")
                sc['reddit_title'] = st.text_input("Reddit", value=sc.get('reddit_title',''))

            st.download_button("⬇️ Export Social Copy JSON", data=json.dumps(sc, indent=2), file_name="social_copy.json", mime="application/json", use_container_width=True)

    # ────────────────────────────────────────────
    # TAB 8: AD COPY
    # ────────────────────────────────────────────
    with tabs[7]:
        st.markdown('<div class="section-chip purple">📢 AD COPY GENERATOR</div>', unsafe_allow_html=True)

        st.markdown("""<div class="info-block">
        Generate ready-to-use ad copy for Google Ads, Facebook/Meta, and display banners.
        </div>""", unsafe_allow_html=True)

        if st.button("📢 Generate Ad Copy (AI)", use_container_width=True):
            if api_key:
                with st.spinner("Writing ad copy..."):
                    ac = generate_ad_copy(data, api_key, model)
                    if ac:
                        st.session_state.ad_copy = ac
                        st.rerun()

        if st.session_state.ad_copy:
            ac = st.session_state.ad_copy

            st.markdown("---")
            st.markdown("**🔍 Google Ads**")
            for i, ad in enumerate(ac.get('google_ads', [])):
                with st.expander(f"Google Ad #{i+1}", expanded=(i==0)):
                    c1,c2,c3 = st.columns(3)
                    with c1: ad['headline1'] = st.text_input(f"H1 ({len(ad.get('headline1',''))}/30)", value=ad.get('headline1',''), key=f"gh1_{i}")
                    with c2: ad['headline2'] = st.text_input(f"H2 ({len(ad.get('headline2',''))}/30)", value=ad.get('headline2',''), key=f"gh2_{i}")
                    with c3: ad['headline3'] = st.text_input(f"H3 ({len(ad.get('headline3',''))}/30)", value=ad.get('headline3',''), key=f"gh3_{i}")
                    ad['desc1'] = st.text_area(f"D1 ({len(ad.get('desc1',''))}/90)", value=ad.get('desc1',''), key=f"gd1_{i}", height=60)
                    ad['desc2'] = st.text_area(f"D2 ({len(ad.get('desc2',''))}/90)", value=ad.get('desc2',''), key=f"gd2_{i}", height=60)

            st.markdown("---")
            st.markdown("**📘 Facebook / Meta Ad**")
            fb = ac.get('facebook', {})
            col_fb1, col_fb2, col_fb3 = st.columns(3)
            with col_fb1: fb['primary_text'] = st.text_area(f"Primary ({len(fb.get('primary_text',''))}/125)", value=fb.get('primary_text',''), height=80)
            with col_fb2: fb['headline'] = st.text_input(f"Headline ({len(fb.get('headline',''))}/40)", value=fb.get('headline',''))
            with col_fb3: fb['description'] = st.text_input(f"Desc ({len(fb.get('description',''))}/30)", value=fb.get('description',''))

            st.markdown("---")
            st.markdown("**🖥️ Display Banner**")
            ac['display_banner'] = st.text_area("Banner Text", value=ac.get('display_banner',''), height=80)

            st.download_button("⬇️ Export Ad Copy JSON", data=json.dumps(ac, indent=2), file_name="ad_copy.json", mime="application/json", use_container_width=True)

    # ────────────────────────────────────────────
    # TAB 9: PREVIEW
    # ────────────────────────────────────────────
    with tabs[8]:
        st.markdown('<div class="section-chip success">👁️ LIVE PREVIEW</div>', unsafe_allow_html=True)

        preview_settings = {
            'brand_color': st.session_state.brand_color,
            'accent_color': st.session_state.accent_color,
            'bg_color': st.session_state.bg_color,
            'text_color': st.session_state.text_color,
            'font_pair': st.session_state.font_pair,
            'hero_layout': st.session_state.hero_layout,
            'animation_style': st.session_state.animation_style,
            'bg_effect': st.session_state.bg_effect,
            'nav_sticky': False,
            'show_nav': st.session_state.show_nav,
            'show_stats': st.session_state.show_stats,
            'show_features': st.session_state.show_features,
            'show_process': st.session_state.show_process,
            'show_testimonials': st.session_state.show_testimonials,
            'show_pricing': st.session_state.show_pricing,
            'show_faq': st.session_state.show_faq,
            'show_cta_banner': st.session_state.show_cta_banner,
            'show_logos': st.session_state.show_logos,
            'show_urgency': st.session_state.show_urgency,
            'cta_url': st.session_state.cta_url,
        }

        col_pv_ctrl1, col_pv_ctrl2, col_pv_ctrl3 = st.columns(3)
        with col_pv_ctrl1:
            pv_height = st.slider("Preview Height (px)", 500, 1800, 950, 50)
        with col_pv_ctrl2:
            pv_zoom = st.select_slider("Zoom", ["50%","75%","100%"], value="100%")
        with col_pv_ctrl3:
            pv_device = st.radio("Device", ["Desktop","Tablet","Mobile"], horizontal=True)

        device_widths = {"Desktop": "100%", "Tablet": "768px", "Mobile": "375px"}
        dw = device_widths.get(pv_device, "100%")

        preview_html = build_html(data, preview_settings)

        if pv_zoom != "100%":
            scale = 0.5 if pv_zoom == "50%" else 0.75
            preview_html_wrapped = f'<div style="transform:scale({scale});transform-origin:top left;width:{int(100/scale)}%;">' + preview_html + '</div>'
        else:
            preview_html_wrapped = preview_html

        st.markdown(f"""
        <div class="preview-toolbar">
          <div class="preview-dot" style="background:#ff5f57"></div>
          <div class="preview-dot" style="background:#febc2e"></div>
          <div class="preview-dot" style="background:#28c840"></div>
          <div class="preview-url">{data.get('brand_name','brand').lower().replace(' ','-')}.com · {pv_device} · {dw}</div>
          <span style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#5a5f7a;">{len(preview_html):,} chars</span>
        </div>
        """, unsafe_allow_html=True)

        if dw != "100%":
            st.markdown(f'<div style="display:flex;justify-content:center;border:1px solid #1e2133;border-top:none;border-radius:0 0 8px 8px;">', unsafe_allow_html=True)
            st.markdown(f'<div style="width:{dw};overflow:hidden;">', unsafe_allow_html=True)
            st.components.v1.html(preview_html, height=pv_height, scrolling=True)
            st.markdown("</div></div>", unsafe_allow_html=True)
        else:
            st.components.v1.html(preview_html, height=pv_height, scrolling=True)

    # ────────────────────────────────────────────
    # TAB 10: CODE
    # ────────────────────────────────────────────
    with tabs[9]:
        st.markdown('<div class="section-chip">💻 CODE OUTPUT</div>', unsafe_allow_html=True)

        final_settings = {
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
            'show_stats': st.session_state.show_stats,
            'show_features': st.session_state.show_features,
            'show_process': st.session_state.show_process,
            'show_testimonials': st.session_state.show_testimonials,
            'show_pricing': st.session_state.show_pricing,
            'show_faq': st.session_state.show_faq,
            'show_cta_banner': st.session_state.show_cta_banner,
            'show_logos': st.session_state.show_logos,
            'show_urgency': st.session_state.show_urgency,
            'cta_url': st.session_state.cta_url,
        }

        final_html = build_html(data, final_settings)
        lines = len(final_html.split('\n'))
        chars = len(final_html)

        col_meta_c1, col_meta_c2, col_meta_c3, col_meta_c4 = st.columns(4)
        with col_meta_c1: st.markdown(f'<div class="stat-box"><div class="stat-num">{lines}</div><div class="stat-label">Lines</div></div>', unsafe_allow_html=True)
        with col_meta_c2: st.markdown(f'<div class="stat-box"><div class="stat-num">{chars//1000}k</div><div class="stat-label">Chars</div></div>', unsafe_allow_html=True)
        with col_meta_c3: st.markdown(f'<div class="stat-box"><div class="stat-num">{len(data.get("features",[]))}</div><div class="stat-label">Features</div></div>', unsafe_allow_html=True)
        with col_meta_c4: st.markdown(f'<div class="stat-box"><div class="stat-num">✓</div><div class="stat-label">Valid HTML5</div></div>', unsafe_allow_html=True)

        show_limit = st.slider("Show lines", 50, lines, min(200, lines), 50)
        visible = "\n".join(final_html.split('\n')[:show_limit])
        if show_limit < lines:
            visible += f"\n\n... ({lines - show_limit} more lines) ..."
        st.code(visible, language="html")

    # ────────────────────────────────────────────
    # TAB 11: EXPORT
    # ────────────────────────────────────────────
    with tabs[10]:
        st.markdown('<div class="section-chip success">📦 EXPORT CENTER</div>', unsafe_allow_html=True)

        final_settings = {
            'brand_color': st.session_state.brand_color, 'accent_color': st.session_state.accent_color,
            'bg_color': st.session_state.bg_color, 'text_color': st.session_state.text_color,
            'font_pair': st.session_state.font_pair, 'hero_layout': st.session_state.hero_layout,
            'animation_style': st.session_state.animation_style, 'bg_effect': st.session_state.bg_effect,
            'nav_sticky': st.session_state.nav_sticky, 'show_nav': st.session_state.show_nav,
            'show_stats': st.session_state.show_stats, 'show_features': st.session_state.show_features,
            'show_process': st.session_state.show_process, 'show_testimonials': st.session_state.show_testimonials,
            'show_pricing': st.session_state.show_pricing, 'show_faq': st.session_state.show_faq,
            'show_cta_banner': st.session_state.show_cta_banner, 'show_logos': st.session_state.show_logos,
            'show_urgency': st.session_state.show_urgency, 'cta_url': st.session_state.cta_url,
        }
        final_html = build_html(data, final_settings)
        ts = datetime.now().strftime('%Y%m%d-%H%M%S')

        col_e = st.columns(3)

        export_items = [
            ("📄 Full HTML Page", "Complete production-ready HTML5 with embedded fonts, CSS animations, and interactive JS. Upload to any host.", final_html, f"landing-page-{ts}.html", "text/html"),
            ("🗃️ Content JSON", "All page content as structured JSON — headline, features, testimonials, pricing, FAQ, stats, and more.", json.dumps(data, indent=2), f"content-{ts}.json", "application/json"),
            ("🎨 Design Config", "Color palette, typography, layout, animation, and section visibility settings as reusable JSON.", json.dumps(final_settings, indent=2), f"design-{ts}.json", "application/json"),
        ]

        for i, (title, desc, content, fname, mime) in enumerate(export_items):
            with col_e[i]:
                st.markdown(f"""<div class="export-card">
                  <div class="export-card-title">{title}</div>
                  <div class="export-card-desc">{desc}</div>
                </div>""", unsafe_allow_html=True)
                st.download_button(f"⬇️ Download", data=content, file_name=fname, mime=mime, use_container_width=True, key=f"dl_{i}")

        st.markdown("---")
        st.markdown('<span class="section-label">📦 Bundle Export</span>', unsafe_allow_html=True)

        all_data = {
            "generated_at": datetime.now().isoformat(),
            "content": data,
            "design": final_settings,
            "seo_meta": st.session_state.seo_meta,
            "ab_variant": st.session_state.ab_variant,
            "email_sequence": st.session_state.email_seq,
            "social_copy": st.session_state.social_copy,
            "ad_copy": st.session_state.ad_copy,
        }

        col_bundle1, col_bundle2 = st.columns(2)
        with col_bundle1:
            st.download_button(
                "⬇️ Full Project Bundle (JSON)",
                data=json.dumps(all_data, indent=2),
                file_name=f"pageforge-project-{ts}.json",
                mime="application/json",
                use_container_width=True,
            )
        with col_bundle2:
            # Changelog / version notes
            changelog_items = [
                ("NEW", "Pricing table section with 3-tier layout"),
                ("NEW", "Process / how-it-works steps"),
                ("NEW", "Urgency banner at top of page"),
                ("NEW", "Logo bar / trusted by section"),
                ("NEW", "A/B test variant generator"),
                ("NEW", "Full SEO meta tag editor"),
                ("NEW", "Email sequence writer"),
                ("NEW", "Social media copy generator"),
                ("NEW", "Ad copy for Google & Facebook"),
                ("NEW", "8 font pairs, 12 color themes"),
                ("NEW", "5 hero layout options"),
                ("NEW", "4 animation styles + scroll triggers"),
                ("NEW", "7 background effects"),
                ("IMP", "Heuristic copy quality scoring"),
                ("IMP", "Version history sidebar"),
                ("IMP", "Per-section AI regeneration"),
                ("IMP", "Responsive device preview mode"),
            ]
            for badge, text in changelog_items[:6]:
                st.markdown(f'<div class="changelog-item"><span class="changelog-badge">{badge}</span><span style="color:#5a5f7a;">{text}</span></div>', unsafe_allow_html=True)

        st.markdown('<div class="tip-block">✅ Your HTML file is <strong>100% standalone</strong> — no server required. Upload to Netlify Drop, Vercel, GitHub Pages, or any static host. Works in any browser.</div>', unsafe_allow_html=True)

else:
    # EMPTY STATE
    st.markdown("""
    <div style="text-align:center;padding:6rem 2rem;">
      <div style="font-size:4.5rem;margin-bottom:1.25rem;">⚡</div>
      <div style="font-family:'Bebas Neue',sans-serif;font-size:2.5rem;letter-spacing:0.08em;color:#e8eaf0;margin-bottom:0.6rem;">READY TO BUILD YOUR PAGE</div>
      <p style="font-family:'Space Mono',monospace;font-size:0.7rem;color:#5a5f7a;letter-spacing:0.12em;text-transform:uppercase;max-width:580px;margin:0 auto 2rem;">
        11 tabs · 8 AI generators · 12 color themes · 8 font pairs · 5 hero layouts · 4 animations · full SEO · email · social · ads
      </p>
      <div style="display:flex;gap:0.75rem;justify-content:center;flex-wrap:wrap;margin-top:1rem;">
        <span style="background:rgba(255,60,95,0.1);border:1px solid rgba(255,60,95,0.25);color:#ff3c5f;padding:0.3rem 0.9rem;border-radius:100px;font-size:0.75rem;font-family:'Space Mono',monospace;">⚡ 1-click AI generation</span>
        <span style="background:rgba(77,124,255,0.1);border:1px solid rgba(77,124,255,0.25);color:#4d7cff;padding:0.3rem 0.9rem;border-radius:100px;font-size:0.75rem;font-family:'Space Mono',monospace;">🎨 Full design control</span>
        <span style="background:rgba(54,211,192,0.1);border:1px solid rgba(54,211,192,0.25);color:#36d3c0;padding:0.3rem 0.9rem;border-radius:100px;font-size:0.75rem;font-family:'Space Mono',monospace;">📦 Production HTML export</span>
        <span style="background:rgba(255,196,77,0.1);border:1px solid rgba(255,196,77,0.25);color:#ffc44d;padding:0.3rem 0.9rem;border-radius:100px;font-size:0.75rem;font-family:'Space Mono',monospace;">🔬 A/B testing</span>
        <span style="background:rgba(150,100,255,0.1);border:1px solid rgba(150,100,255,0.25);color:#9664ff;padding:0.3rem 0.9rem;border-radius:100px;font-size:0.75rem;font-family:'Space Mono',monospace;">📢 Google & FB ads</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# FOOTER
st.markdown("""<div style="text-align:center;padding:1.5rem 0 0.5rem;">
  <span style="font-family:'Space Mono',monospace;font-size:0.58rem;color:#1e2133;letter-spacing:0.18em;text-transform:uppercase;">
    PAGEFORGE V2 · AI LANDING PAGE STUDIO · BUILT WITH STREAMLIT + OPENAI
  </span>
</div>""", unsafe_allow_html=True)
