import streamlit as st
from PIL import Image
import io, os, base64
from streamlit.components.v1 import html as st_html

# ─── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🎉 Elease Benford – 80th Birthday Frame",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Cormorant+Garamond:ital,wght@1,300&display=swap');
html, body, [data-testid="stAppViewContainer"] { background: #062918 !important; }
[data-testid="stAppViewContainer"] > .main { background: #062918; }
[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer { visibility: hidden; }
h1 { font-family:'Cinzel',serif !important; font-size:2rem !important; font-weight:900 !important; color:#ffe066 !important; text-align:center; letter-spacing:0.1em; text-shadow:0 0 30px rgba(255,224,102,0.6); margin-bottom:0 !important; }
.subtitle { font-family:'Cormorant Garamond',serif; font-style:italic; font-size:1.1rem; color:rgba(201,168,76,0.7); text-align:center; letter-spacing:0.06em; margin-bottom:18px; }
.gold-divider { height:1px; background:linear-gradient(90deg,transparent,#c9a84c,transparent); margin:16px 0; opacity:0.6; }
.stButton > button { font-family:'Cinzel',serif !important; font-weight:700 !important; letter-spacing:0.08em !important; text-transform:uppercase !important; background:linear-gradient(135deg,#8b6914,#c9a84c,#8b6914) !important; color:#062918 !important; border:none !important; border-radius:4px !important; box-shadow:0 4px 20px rgba(201,168,76,0.35) !important; width:100% !important; }
.stButton > button:hover { box-shadow:0 8px 32px rgba(201,168,76,0.65) !important; }
.stFileUploader [data-testid="stFileUploaderDropzone"] { background:#0d3d20 !important; border:1px dashed #c9a84c !important; border-radius:6px !important; }
.stFileUploader [data-testid="stFileUploaderDropzone"] * { color:#f0d080 !important; }
.section-label { font-family:'Cinzel',serif; font-size:0.75rem; letter-spacing:0.12em; color:rgba(201,168,76,0.55); text-transform:uppercase; margin-bottom:8px; }
.sparkle-bg { position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:-1;overflow:hidden; }
.stTabs [data-baseweb="tab-list"] { background:transparent !important; border-bottom:1px solid rgba(201,168,76,0.3) !important; gap:4px; }
.stTabs [data-baseweb="tab"] { font-family:'Cinzel',serif !important; font-size:0.78rem !important; letter-spacing:0.1em !important; color:rgba(201,168,76,0.5) !important; background:transparent !important; border:none !important; padding:8px 20px !important; }
.stTabs [aria-selected="true"] { color:#ffe066 !important; border-bottom:2px solid #c9a84c !important; background:rgba(201,168,76,0.07) !important; }
</style>
<div class="sparkle-bg" id="spbg"></div>
<script>
(function(){
    const bg=document.getElementById('spbg');if(!bg)return;
    const s=document.createElement('style');s.textContent='@keyframes tw{0%,100%{opacity:0;transform:scale(.4)}50%{opacity:.6;transform:scale(1.3)}}';document.head.appendChild(s);
    for(let i=0;i<70;i++){const d=document.createElement('div');const sz=Math.random()*3+1;d.style.cssText=`position:absolute;border-radius:50%;background:#ffe066;width:${sz}px;height:${sz}px;left:${Math.random()*100}%;top:${Math.random()*100}%;opacity:0;animation:tw ${2+Math.random()*4}s ease-in-out ${-Math.random()*5}s infinite;`;bg.appendChild(d);}
})();
</script>
""", unsafe_allow_html=True)

# ─── Load frame ────────────────────────────────────────────────────────────────
FRAME_PATH = os.path.join(os.path.dirname(__file__), "frame.png")
frame_pil  = Image.open(FRAME_PATH).convert("RGBA")
CUTOUT = dict(top=106, bottom=961, left=269, right=785)

def apply_frame(photo: Image.Image) -> Image.Image:
    cut_w = CUTOUT["right"] - CUTOUT["left"]
    cut_h = CUTOUT["bottom"] - CUTOUT["top"]
    ratio = cut_w / cut_h
    pw, ph = photo.size
    if pw / ph > ratio:
        nw = int(ph * ratio)
        photo = photo.crop(((pw-nw)//2, 0, (pw-nw)//2+nw, ph))
    else:
        nh = int(pw / ratio)
        photo = photo.crop((0, (ph-nh)//2, pw, (ph-nh)//2+nh))
    photo  = photo.resize((cut_w, cut_h), Image.Resampling.LANCZOS).convert("RGBA")
    canvas = Image.new("RGBA", frame_pil.size, (0,0,0,0))
    canvas.paste(photo, (CUTOUT["left"], CUTOUT["top"]), photo)
    return Image.alpha_composite(canvas, frame_pil).convert("RGB")

# ─── Session state ─────────────────────────────────────────────────────────────
if "gallery" not in st.session_state:
    st.session_state.gallery = []

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("<h1>🎉 80th Birthday Photo Frame</h1>", unsafe_allow_html=True)
st.markdown('<div class="subtitle">Elease Benford · Celebrating 80 Magnificent Years</div>', unsafe_allow_html=True)
st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab_cam, tab_upload = st.tabs(["📷 Take Photo", "🖼 Upload Photo"])

photo_source = None

# ── Camera tab ─────────────────────────────────────────────────────────────────
with tab_cam:
    # This custom HTML component directly calls getUserMedia with facingMode: environment
    # The captured image is posted back as a base64 data URL via Streamlit's component value
    camera_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&display=swap" rel="stylesheet">
    <style>
      * { margin:0; padding:0; box-sizing:border-box; }
      body { background:#062918; padding:4px; }
      #video { width:100%; border-radius:6px; border:1px solid rgba(201,168,76,0.3); display:block; }
      #preview { width:100%; border-radius:6px; border:1px solid rgba(201,168,76,0.5); display:none; margin-top:8px; }
      #canvas { display:none; }
      .btn {
        margin-top:8px; width:100%; padding:10px;
        background:linear-gradient(135deg,#8b6914,#c9a84c,#8b6914);
        color:#062918; border:none; border-radius:4px;
        font-family:'Cinzel',serif; font-weight:700; font-size:0.85rem;
        letter-spacing:0.1em; text-transform:uppercase; cursor:pointer;
      }
      .btn:active { opacity:0.8; }
      #status { color:rgba(201,168,76,0.6); font-size:0.72rem; font-family:'Cinzel',serif;
                text-align:center; margin-top:6px; letter-spacing:0.08em; }
      #retake { display:none; }
    </style>
    </head>
    <body>
    <video id="video" autoplay playsinline muted></video>
    <img id="preview" />
    <canvas id="canvas"></canvas>
    <button class="btn" id="capture">📸 Capture Photo</button>
    <button class="btn" id="retake">🔄 Retake</button>
    <div id="status">Starting rear camera…</div>

    <script>
    const video   = document.getElementById('video');
    const canvas  = document.getElementById('canvas');
    const preview = document.getElementById('preview');
    const capBtn  = document.getElementById('capture');
    const retakeBtn = document.getElementById('retake');
    const status  = document.getElementById('status');

    async function startCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: { ideal: 'environment' }, width:{ideal:1920}, height:{ideal:1080} },
          audio: false
        });
        video.srcObject = stream;
        await new Promise(r => video.onloadedmetadata = r);
        const track = stream.getVideoTracks()[0];
        const s = track.getSettings();
        status.textContent = s.facingMode === 'environment' ? '📷 Rear camera active' : '📷 Camera active';
      } catch(e) {
        status.textContent = '⚠ ' + e.message;
      }
    }

    capBtn.addEventListener('click', () => {
      canvas.width  = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video, 0, 0);
      const dataUrl = canvas.toDataURL('image/jpeg', 0.92);

      // Show preview, hide live feed
      preview.src = dataUrl;
      preview.style.display = 'block';
      video.style.display = 'none';
      capBtn.style.display = 'none';
      retakeBtn.style.display = 'block';
      status.textContent = '✅ Photo captured — scroll down to see it framed!';

      // Send to Streamlit
      Streamlit.setComponentValue(dataUrl);
    });

    retakeBtn.addEventListener('click', () => {
      preview.style.display = 'none';
      video.style.display = 'block';
      capBtn.style.display = 'block';
      retakeBtn.style.display = 'none';
      status.textContent = '📷 Ready — aim and capture';
      Streamlit.setComponentValue(null);
    });

    startCamera();
    Streamlit.setFrameHeight(document.body.scrollHeight + 20);
    window.addEventListener('resize', () => Streamlit.setFrameHeight(document.body.scrollHeight + 20));
    </script>
    </body>
    </html>
    """

    captured_b64 = st_html(camera_html, height=420)

    if captured_b64 and isinstance(captured_b64, str) and captured_b64.startswith("data:image"):
        try:
            _, data = captured_b64.split(",", 1)
            photo_source = Image.open(io.BytesIO(base64.b64decode(data))).convert("RGB")
        except Exception as ex:
            st.error(f"Could not decode captured image: {ex}")

# ── Upload tab ─────────────────────────────────────────────────────────────────
with tab_upload:
    uploaded = st.file_uploader("Upload a photo", type=["jpg","jpeg","png"])
    if uploaded:
        photo_source = Image.open(uploaded).convert("RGB")

# ─── Frame & display ──────────────────────────────────────────────────────────
if photo_source:
    framed = apply_frame(photo_source)
    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
    st.image(framed, use_column_width=True)

    col1, col2 = st.columns(2)
    with col1:
        buf = io.BytesIO()
        framed.save(buf, format="PNG")
        buf.seek(0)
        st.download_button("⬇ Download Photo", data=buf,
                           file_name="birthday_elease_framed.png", mime="image/png",
                           use_container_width=True)
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
            st.download_button("⬇ Save", data=buf,
                               file_name=f"birthday_elease_{i+1}.png", mime="image/png",
                               key=f"dl_{i}", use_container_width=True)
    if st.button("🗑 Clear Gallery"):
        st.session_state.gallery = []
        st.rerun()

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
st.markdown(
    '<div style="font-family:\'Cormorant Garamond\',serif;font-style:italic;'
    'font-size:0.85rem;color:rgba(201,168,76,0.35);text-align:center;letter-spacing:0.04em;">'
    '🌿 Celebrating 80 magnificent years of love, grace, and joy 🌿</div>',
    unsafe_allow_html=True)
