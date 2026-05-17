import streamlit as st
from PIL import Image
import io
import os

# ─── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🎉 Elease Benford – 80th Birthday Frame",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Cormorant+Garamond:ital,wght@1,300&display=swap');

html, body, [data-testid="stAppViewContainer"] { background: #062918 !important; }
[data-testid="stAppViewContainer"] > .main { background: #062918; }
[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer { visibility: hidden; }

h1 {
    font-family: 'Cinzel', serif !important;
    font-size: 2rem !important;
    font-weight: 900 !important;
    color: #ffe066 !important;
    text-align: center;
    letter-spacing: 0.1em;
    text-shadow: 0 0 30px rgba(255,224,102,0.6);
    margin-bottom: 0 !important;
}
.subtitle {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-size: 1.1rem;
    color: rgba(201,168,76,0.7);
    text-align: center;
    letter-spacing: 0.06em;
    margin-bottom: 18px;
}
.gold-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #c9a84c, transparent);
    margin: 16px 0;
    opacity: 0.6;
}
.stButton > button {
    font-family: 'Cinzel', serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    background: linear-gradient(135deg, #8b6914, #c9a84c, #8b6914) !important;
    color: #062918 !important;
    border: none !important;
    border-radius: 4px !important;
    box-shadow: 0 4px 20px rgba(201,168,76,0.35) !important;
    width: 100% !important;
}
.stButton > button:hover {
    box-shadow: 0 8px 32px rgba(201,168,76,0.65) !important;
}
.stFileUploader [data-testid="stFileUploaderDropzone"] {
    background: #0d3d20 !important;
    border: 1px dashed #c9a84c !important;
    border-radius: 6px !important;
}
.stFileUploader [data-testid="stFileUploaderDropzone"] * { color: #f0d080 !important; }
.section-label {
    font-family: 'Cinzel', serif;
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    color: rgba(201,168,76,0.55);
    text-transform: uppercase;
    margin-bottom: 8px;
}
.sparkle-bg { position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:-1;overflow:hidden; }
</style>

<div class="sparkle-bg" id="spbg"></div>
<script>
(function(){
    const bg=document.getElementById('spbg');
    if(!bg)return;
    const style=document.createElement('style');
    style.textContent='@keyframes tw{0%,100%{opacity:0;transform:scale(.4)}50%{opacity:.6;transform:scale(1.3)}}';
    document.head.appendChild(style);
    for(let i=0;i<70;i++){
        const s=document.createElement('div');
        const sz=Math.random()*3+1;
        s.style.cssText=`position:absolute;border-radius:50%;background:#ffe066;width:${sz}px;height:${sz}px;left:${Math.random()*100}%;top:${Math.random()*100}%;opacity:0;animation:tw ${2+Math.random()*4}s ease-in-out ${-Math.random()*5}s infinite;`;
        bg.appendChild(s);
    }
})();
</script>
""", unsafe_allow_html=True)

# ─── Load frame ────────────────────────────────────────────────────────────────
FRAME_PATH = os.path.join(os.path.dirname(__file__), "frame.png")
frame_pil  = Image.open(FRAME_PATH).convert("RGBA")

CUTOUT = dict(top=106, bottom=961, left=269, right=785)

def apply_frame(photo: Image.Image) -> Image.Image:
    cut_w = CUTOUT["right"]  - CUTOUT["left"]
    cut_h = CUTOUT["bottom"] - CUTOUT["top"]
    ratio = cut_w / cut_h
    pw, ph = photo.size
    if pw / ph > ratio:
        nw = int(ph * ratio)
        photo = photo.crop(((pw - nw) // 2, 0, (pw - nw) // 2 + nw, ph))
    else:
        nh = int(pw / ratio)
        photo = photo.crop((0, (ph - nh) // 2, pw, (ph - nh) // 2 + nh))
    photo  = photo.resize((cut_w, cut_h), Image.Resampling.LANCZOS).convert("RGBA")
    canvas = Image.new("RGBA", frame_pil.size, (0, 0, 0, 0))
    canvas.paste(photo, (CUTOUT["left"], CUTOUT["top"]), photo)
    return Image.alpha_composite(canvas, frame_pil).convert("RGB")

# ─── Session state ─────────────────────────────────────────────────────────────
if "gallery" not in st.session_state:
    st.session_state.gallery = []

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("<h1>🎉 80th Birthday Photo Frame</h1>", unsafe_allow_html=True)
st.markdown('<div class="subtitle">Elease Benford · Celebrating 80 Magnificent Years</div>',
            unsafe_allow_html=True)
st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

# ─── Upload ───────────────────────────────────────────────────────────────────
uploaded = st.file_uploader(
    "Upload a photo to apply the frame",
    type=["jpg", "jpeg", "png"],
)

if uploaded:
    photo  = Image.open(uploaded).convert("RGB")
    framed = apply_frame(photo)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
    st.image(framed, use_column_width=True)

    col1, col2 = st.columns(2)

    with col1:
        buf = io.BytesIO()
        framed.save(buf, format="PNG")
        buf.seek(0)
        st.download_button(
            label="⬇ Download Photo",
            data=buf,
            file_name="birthday_elease_framed.png",
            mime="image/png",
            use_container_width=True,
        )

    with col2:
        if st.button("➕ Save to Gallery", key="add_gallery"):
            st.session_state.gallery.insert(0, framed)
            st.success("Saved!")
            st.rerun()

# ─── Gallery ──────────────────────────────────────────────────────────────────
if st.session_state.gallery:
    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">🖼 Gallery</div>', unsafe_allow_html=True)

    cols = st.columns(min(len(st.session_state.gallery), 3))
    for i, img in enumerate(st.session_state.gallery[:9]):
        with cols[i % 3]:
            st.image(img, use_column_width=True)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            st.download_button(
                "⬇ Save",
                data=buf,
                file_name=f"birthday_elease_{i+1}.png",
                mime="image/png",
                key=f"dl_{i}",
                use_container_width=True,
            )

    if st.button("🗑 Clear Gallery"):
        st.session_state.gallery = []
        st.rerun()

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
st.markdown(
    '<div style="font-family:\'Cormorant Garamond\',serif;font-style:italic;'
    'font-size:0.85rem;color:rgba(201,168,76,0.35);text-align:center;letter-spacing:0.04em;">'
    '🌿 Celebrating 80 magnificent years of love, grace, and joy 🌿</div>',
    unsafe_allow_html=True,
)
