import streamlit as st
from PIL import Image, ImageOps
import io, os, base64
from streamlit.components.v1 import html as st_html

st.set_page_config(
    page_title="🎉 Elease Benford – 80th Birthday",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Read frame as base64 so we can pass it into the JS component ───────────────
FRAME_PATH = os.path.join(os.path.dirname(__file__), "frame.png")
with open(FRAME_PATH, "rb") as f:
    FRAME_B64 = base64.b64encode(f.read()).decode()

CUTOUT = dict(top=106, bottom=961, left=269, right=785)   # adjust if frame changes

# ── Page-level CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Cormorant+Garamond:ital,wght@1,300;0,400&display=swap');

:root {
  --gold:   #c9a84c;
  --gold2:  #ffe066;
  --green:  #062918;
  --green2: #0d3d20;
}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
    background: var(--green) !important;
}
[data-testid="stHeader"]          { background: transparent !important; }
[data-testid="stMainBlockContainer"] { padding-top: 1.5rem !important; }
#MainMenu, footer                 { visibility: hidden; }

/* headings */
h1 {
    font-family: 'Cinzel', serif !important;
    font-size: clamp(1.4rem, 5vw, 2.2rem) !important;
    font-weight: 900 !important;
    color: var(--gold2) !important;
    text-align: center;
    letter-spacing: .12em;
    text-shadow: 0 0 40px rgba(255,224,102,.55);
    margin-bottom: 0 !important;
    line-height: 1.2 !important;
}
h3 {
    font-family: 'Cinzel', serif !important;
    font-size: .72rem !important;
    font-weight: 700 !important;
    color: rgba(201,168,76,.45) !important;
    letter-spacing: .18em !important;
    text-transform: uppercase !important;
    margin-bottom: 6px !important;
}
.subtitle {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-size: clamp(.9rem, 3vw, 1.15rem);
    color: rgba(201,168,76,.65);
    text-align: center;
    letter-spacing: .06em;
}
.gold-line {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    opacity: .55;
    margin: 14px 0;
}
.ornament {
    text-align: center;
    font-size: 1.1rem;
    color: rgba(201,168,76,.35);
    letter-spacing: .5em;
}

/* Buttons */
.stButton > button {
    font-family: 'Cinzel', serif !important;
    font-weight: 700 !important;
    letter-spacing: .1em !important;
    text-transform: uppercase !important;
    background: linear-gradient(135deg, #7a5c10, var(--gold), #7a5c10) !important;
    color: var(--green) !important;
    border: none !important;
    border-radius: 3px !important;
    padding: 10px 0 !important;
    box-shadow: 0 4px 22px rgba(201,168,76,.3) !important;
    width: 100% !important;
    transition: box-shadow .2s !important;
}
.stButton > button:hover {
    box-shadow: 0 8px 36px rgba(201,168,76,.6) !important;
}

/* File uploader */
.stFileUploader [data-testid="stFileUploaderDropzone"] {
    background: var(--green2) !important;
    border: 1px dashed var(--gold) !important;
    border-radius: 6px !important;
}
.stFileUploader [data-testid="stFileUploaderDropzone"] * { color: #f0d080 !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(201,168,76,.25) !important;
    gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Cinzel', serif !important;
    font-size: .76rem !important;
    letter-spacing: .12em !important;
    color: rgba(201,168,76,.4) !important;
    background: transparent !important;
    border: none !important;
    padding: 9px 22px !important;
}
.stTabs [aria-selected="true"] {
    color: var(--gold2) !important;
    border-bottom: 2px solid var(--gold) !important;
    background: rgba(201,168,76,.06) !important;
}

/* Sparkle background */
.spbg { position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;overflow:hidden; }
[data-testid="stAppViewContainer"] { position: relative; z-index: 1; }
</style>

<!-- Sparkle canvas -->
<div class="spbg" id="spbg"></div>
<script>
(function(){
  const bg = document.getElementById('spbg');
  if (!bg) return;
  const st = document.createElement('style');
  st.textContent = '@keyframes tw{0%,100%{opacity:0;transform:scale(.3) rotate(0deg)}50%{opacity:.55;transform:scale(1.4) rotate(180deg)}}';
  document.head.appendChild(st);
  for (let i = 0; i < 90; i++) {
    const d = document.createElement('div');
    const sz = Math.random() * 3 + 1;
    d.style.cssText = `position:absolute;border-radius:50%;background:#ffe066;width:${sz}px;height:${sz}px;`
      + `left:${Math.random()*100}%;top:${Math.random()*100}%;opacity:0;`
      + `animation:tw ${2.5+Math.random()*4}s ease-in-out ${-Math.random()*6}s infinite;`;
    bg.appendChild(d);
  }
})();
</script>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def apply_frame(photo: Image.Image) -> Image.Image:
    """Composite photo into frame cutout WITHOUT rotating."""
    # Fix EXIF orientation so portrait photos stay portrait
    photo = ImageOps.exif_transpose(photo)

    cut_w = CUTOUT["right"]  - CUTOUT["left"]
    cut_h = CUTOUT["bottom"] - CUTOUT["top"]
    ratio = cut_w / cut_h
    pw, ph = photo.size

    # Centre-crop to match cutout aspect ratio
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


def img_to_dl_bytes(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ── Load frame PIL (for upload path) ──────────────────────────────────────────
frame_pil = Image.open(FRAME_PATH).convert("RGBA")

# ── Session state ─────────────────────────────────────────────────────────────
if "gallery"  not in st.session_state: st.session_state.gallery  = []
if "cam_snap" not in st.session_state: st.session_state.cam_snap = None

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<h1>✦ 80th Birthday Frame ✦</h1>", unsafe_allow_html=True)
st.markdown('<div class="subtitle">Elease Benford &nbsp;·&nbsp; Eighty Magnificent Years</div>',
            unsafe_allow_html=True)
st.markdown('<div class="ornament">· · · ✦ · · ·</div>', unsafe_allow_html=True)
st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab_cam, tab_upload = st.tabs(["📷  Live Camera", "🖼  Upload Photo"])
photo_source = None   # PIL Image set by either tab

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 – LIVE CAMERA  (frame overlay rendered in real-time on canvas)
# ─────────────────────────────────────────────────────────────────────────────
with tab_cam:

    # Pass frame image + cutout into the component via template literals
    COMP_HTML = f"""<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&display=swap" rel="stylesheet">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}

  html, body {{
    background: #062918;
    font-family: 'Cinzel', serif;
    height: 100%;
    overflow-x: hidden;
  }}

  /* Full layout: canvas takes all space, button bar fixed at bottom */
  #wrap {{
    position: relative;
    width: 100%;
    padding-bottom: 90px; /* room for button bar */
  }}

  /* Canvases fill the width, natural aspect ratio */
  #liveCanvas, #snapCanvas {{
    width: 100%;
    display: block;
    border-radius: 6px;
    box-shadow: 0 6px 32px rgba(0,0,0,.7);
  }}
  #snapCanvas {{ display: none; }}

  /* ── BIG capture button – fixed at bottom of iframe ── */
  #btnBar {{
    position: fixed;
    bottom: 0; left: 0; right: 0;
    padding: 10px 12px 14px;
    background: linear-gradient(to top, #062918 70%, transparent);
    display: flex;
    gap: 10px;
    z-index: 99;
  }}

  .btn {{
    flex: 1;
    padding: 15px 8px;
    border: none;
    border-radius: 6px;
    font-family: 'Cinzel', serif;
    font-weight: 700;
    font-size: .88rem;
    letter-spacing: .1em;
    text-transform: uppercase;
    cursor: pointer;
    transition: opacity .15s, box-shadow .2s;
    -webkit-tap-highlight-color: transparent;
  }}
  .btn:active {{ opacity: .7; }}

  #snapBtn {{
    background: linear-gradient(135deg, #7a5c10, #e8c05a, #7a5c10);
    color: #062918;
    box-shadow: 0 4px 24px rgba(201,168,76,.55);
    font-size: 1rem;
    flex: 2;  /* wider than flip */
  }}
  #snapBtn:hover {{ box-shadow: 0 8px 36px rgba(201,168,76,.8); }}

  .btn.sec {{
    background: rgba(201,168,76,.12);
    border: 1px solid rgba(201,168,76,.4);
    color: rgba(201,168,76,.85);
    box-shadow: none;
    flex: 1;
  }}

  #status {{
    text-align: center;
    color: rgba(201,168,76,.5);
    font-size: .65rem;
    letter-spacing: .1em;
    padding: 5px 8px 0;
    min-height: 1.2em;
  }}
</style>
</head>
<body>

<div id="wrap">
  <canvas id="liveCanvas"></canvas>
  <canvas id="snapCanvas"></canvas>
  <div id="status">Starting rear camera…</div>
</div>

<!-- Fixed bottom button bar — always visible no matter iframe height -->
<div id="btnBar">
  <button class="btn sec" id="flipBtn">🔁 Flip</button>
  <button class="btn" id="snapBtn">📸 CAPTURE PHOTO</button>
  <button class="btn sec" id="retakeBtn" style="display:none">🔄 Retake</button>
</div>

<!-- Hidden video element – feeds the canvas -->
<video id="vid" autoplay playsinline muted style="display:none;position:absolute;"></video>

<script>
const liveC   = document.getElementById('liveCanvas');
const snapC   = document.getElementById('snapCanvas');
const liveCtx = liveC.getContext('2d');
const snapCtx = snapC.getContext('2d');
const vid     = document.getElementById('vid');
const snapBtn = document.getElementById('snapBtn');
const retakeBtn = document.getElementById('retakeBtn');
const flipBtn = document.getElementById('flipBtn');
const status  = document.getElementById('status');

// ── Frame image ─────────────────────────────────────────────────────────────
const frameImg = new Image();
frameImg.src   = 'data:image/png;base64,{FRAME_B64}';

// Cutout coords (pixels in the full-res frame image)
const CUT = {{ top:{CUTOUT['top']}, bottom:{CUTOUT['bottom']}, left:{CUTOUT['left']}, right:{CUTOUT['right']} }};
const CUT_W = CUT.right  - CUT.left;   // width of the photo slot
const CUT_H = CUT.bottom - CUT.top;    // height of the photo slot
const CUT_RATIO = CUT_W / CUT_H;       // aspect ratio of slot

// ── Camera state ────────────────────────────────────────────────────────────
let stream       = null;
let facingMode   = 'environment';   // start with rear camera
let animId       = null;
let snapped      = false;

async function startCamera(facing) {{
  if (stream) {{ stream.getTracks().forEach(t => t.stop()); }}
  status.textContent = 'Starting ' + (facing==='environment' ? 'rear' : 'front') + ' camera…';
  try {{
    stream = await navigator.mediaDevices.getUserMedia({{
      video: {{
        facingMode: {{ ideal: facing }},
        width:  {{ ideal: 1920 }},
        height: {{ ideal: 1080 }}
      }},
      audio: false
    }});
    vid.srcObject = stream;
    await new Promise(r => {{ vid.onloadedmetadata = r; }});
    await vid.play();

    const t = stream.getVideoTracks()[0];
    const s = t.getSettings();
    facingMode = s.facingMode || facing;
    status.textContent = facingMode === 'environment' ? '📷 Rear camera — aim & capture' : '🤳 Front camera active';

    if (!snapped) startLive();
  }} catch(e) {{
    status.textContent = '⚠ ' + e.message;
  }}
}}

// ── Live compositing loop ────────────────────────────────────────────────────
function startLive() {{
  if (animId) cancelAnimationFrame(animId);

  function draw() {{
    if (snapped) return;
    animId = requestAnimationFrame(draw);

    const vw = vid.videoWidth;
    const vh = vid.videoHeight;
    if (!vw || !vh || !frameImg.complete) return;

    // Frame aspect ratio drives the canvas size
    const FW = frameImg.naturalWidth  || 1054;
    const FH = frameImg.naturalHeight || 1067;

    // Set canvas resolution once
    if (liveC.width !== FW) {{ liveC.width = FW; liveC.height = FH; }}

    // --- Draw video into the cutout, centre-cropped, NO rotation ---
    const vRatio = vw / vh;

    let sx, sy, sw, sh;
    if (vRatio > CUT_RATIO) {{
      // video is wider than slot → crop sides
      sh = vh;
      sw = Math.round(vh * CUT_RATIO);
      sx = Math.round((vw - sw) / 2);
      sy = 0;
    }} else {{
      // video is taller than slot → crop top/bottom
      sw = vw;
      sh = Math.round(vw / CUT_RATIO);
      sx = 0;
      sy = Math.round((vh - sh) / 2);
    }}

    liveCtx.drawImage(vid, sx, sy, sw, sh, CUT.left, CUT.top, CUT_W, CUT_H);

    // --- Overlay frame on top ---
    liveCtx.drawImage(frameImg, 0, 0, FW, FH);
  }}

  draw();
}}

// ── Capture ──────────────────────────────────────────────────────────────────
snapBtn.addEventListener('click', () => {{
  if (!vid.videoWidth) return;
  snapped = true;
  if (animId) cancelAnimationFrame(animId);

  const FW = frameImg.naturalWidth  || 1054;
  const FH = frameImg.naturalHeight || 1067;
  snapC.width  = FW;
  snapC.height = FH;

  const vw = vid.videoWidth, vh = vid.videoHeight;
  const vRatio = vw / vh;
  let sx, sy, sw, sh;
  if (vRatio > CUT_RATIO) {{
    sh = vh; sw = Math.round(vh * CUT_RATIO); sx = Math.round((vw-sw)/2); sy = 0;
  }} else {{
    sw = vw; sh = Math.round(vw/CUT_RATIO); sx = 0; sy = Math.round((vh-sh)/2);
  }}

  snapCtx.drawImage(vid, sx, sy, sw, sh, CUT.left, CUT.top, CUT_W, CUT_H);
  snapCtx.drawImage(frameImg, 0, 0, FW, FH);

  // Show snap, hide live
  liveC.style.display     = 'none';
  snapC.style.display     = 'block';
  snapBtn.style.display   = 'none';
  retakeBtn.style.display = 'flex';
  flipBtn.style.display   = 'none';
  status.textContent = '✅ Captured! Scroll down to download & save.';

  // Send base64 JPEG back to Streamlit
  const dataUrl = snapC.toDataURL('image/jpeg', 0.95);
  Streamlit.setComponentValue(dataUrl);
}});

// ── Retake ───────────────────────────────────────────────────────────────────
retakeBtn.addEventListener('click', () => {{
  snapped = false;
  liveC.style.display     = 'block';
  snapC.style.display     = 'none';
  snapBtn.style.display   = 'flex';
  retakeBtn.style.display = 'none';
  flipBtn.style.display   = 'flex';
  status.textContent = '📷 Ready — aim and capture';
  Streamlit.setComponentValue(null);
  startLive();
}});

// ── Flip camera ──────────────────────────────────────────────────────────────
flipBtn.addEventListener('click', () => {{
  facingMode = facingMode === 'environment' ? 'user' : 'environment';
  startCamera(facingMode);
}});

// ── Boot ─────────────────────────────────────────────────────────────────────
frameImg.onload = () => startCamera('environment');
if (frameImg.complete) startCamera('environment');

// Tell Streamlit how tall the iframe should be
// We do NOT use setFrameHeight dynamically — just set a fixed tall value via the height param
</script>
</body>
</html>"""

    result = st_html(COMP_HTML, height=900)

    if result and isinstance(result, str) and result.startswith("data:image"):
        try:
            _, data = result.split(",", 1)
            img_bytes = base64.b64decode(data)
            # ImageOps.exif_transpose guards against any EXIF rotation
            photo_source = ImageOps.exif_transpose(Image.open(io.BytesIO(img_bytes)).convert("RGB"))
            st.session_state.cam_snap = photo_source
        except Exception as ex:
            st.error(f"Could not decode image: {ex}")
    elif st.session_state.cam_snap is not None and result is None:
        # retake was pressed – clear
        st.session_state.cam_snap = None

    # Use cam snap if available (persists across reruns)
    if photo_source is None and st.session_state.cam_snap is not None:
        photo_source = st.session_state.cam_snap

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 – UPLOAD
# ─────────────────────────────────────────────────────────────────────────────
with tab_upload:
    st.markdown("")
    uploaded = st.file_uploader("Choose a photo", type=["jpg","jpeg","png"])
    if uploaded:
        raw = Image.open(uploaded)
        raw = ImageOps.exif_transpose(raw).convert("RGB")
        photo_source = raw

# ══════════════════════════════════════════════════════════════════════════════
# RESULT — framed photo + download
# ══════════════════════════════════════════════════════════════════════════════
if photo_source:
    # For upload tab — camera tab already composites on JS side, but we still
    # run apply_frame so both tabs produce identical server-side PNG for download.
    framed = apply_frame(photo_source)

    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)
    st.markdown("### 🖼 Your Framed Photo")
    st.image(framed, use_column_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "⬇  Download",
            data=img_to_dl_bytes(framed),
            file_name="elease_80th_birthday.png",
            mime="image/png",
            use_container_width=True,
        )
    with col2:
        if st.button("➕  Save to Gallery"):
            st.session_state.gallery.insert(0, framed)
            st.success("Saved to gallery!")
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# GALLERY
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.gallery:
    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)
    st.markdown("### 📸 Gallery")

    for row_start in range(0, min(len(st.session_state.gallery), 9), 3):
        row_imgs = st.session_state.gallery[row_start:row_start+3]
        cols = st.columns(len(row_imgs))
        for i, img in enumerate(row_imgs):
            with cols[i]:
                st.image(img, use_column_width=True)
                st.download_button(
                    "⬇",
                    data=img_to_dl_bytes(img),
                    file_name=f"elease_80th_{row_start+i+1}.png",
                    mime="image/png",
                    key=f"dl_{row_start+i}",
                    use_container_width=True,
                )

    st.markdown("")
    if st.button("🗑  Clear Gallery"):
        st.session_state.gallery = []
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:18px 0 28px;">
  <div style="font-family:'Cinzel',serif;font-size:.65rem;letter-spacing:.22em;
              color:rgba(201,168,76,.3);text-transform:uppercase;margin-bottom:8px;">
    Celebrating Eight Decades
  </div>
  <div style="font-family:'Cormorant Garamond',serif;font-style:italic;
              font-size:1rem;color:rgba(201,168,76,.4);letter-spacing:.05em;">
    🌿 &nbsp; Eighty years of love, grace, wisdom &amp; joy &nbsp; 🌿
  </div>
  <div style="margin-top:12px;font-size:.7rem;color:rgba(201,168,76,.18);
              letter-spacing:.15em;font-family:'Cinzel',serif;">
    ✦ &nbsp; Elease Benford &nbsp; ✦
  </div>
</div>
""", unsafe_allow_html=True)
