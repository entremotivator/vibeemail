import streamlit as st
from PIL import Image
import io
import os
import base64
from streamlit.components.v1 import html as st_html

# ── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="✦ Apostle Victor A. Howard Sr. – Birthday Celebration",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Frame Setup ────────────────────────────────────────────────
FRAME_PATH = os.path.join(os.path.dirname(__file__), "apostle_victor_frame.png")
FRAME_OK = os.path.exists(FRAME_PATH)

if FRAME_OK:
    frame_img = Image.open(FRAME_PATH)
    frame_b64 = base64.b64encode(open(FRAME_PATH, "rb").read()).decode()

# ── Global CSS: Full-screen immersive design ───────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,400&family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&display=swap');

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main,
[data-testid="stMainBlockContainer"],
.stMainBlockContainer {
  margin: 0 !important;
  padding: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  overflow: hidden !important;
  background: #0a0a0a !important;
}

[data-testid="stAppViewContainer"] > .main {
  display: flex;
  align-items: center;
  justify-content: center;
}

.stMainBlockContainer {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 !important;
}

/* Hide Streamlit chrome */
header, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {
  display: none !important;
}

/* Container styling */
.main-container {
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  overflow: hidden;
}

.frame-container {
  position: relative;
  width: 90vmin;
  height: auto;
  max-width: 600px;
  max-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Typography */
h1, h2, h3 {
  font-family: 'Playfair Display', serif !important;
  color: #d4af37 !important;
  text-align: center !important;
  text-transform: uppercase !important;
  letter-spacing: 2px !important;
}

h1 {
  font-size: 2.5rem !important;
  font-weight: 900 !important;
  margin: 0 !important;
}

h2 {
  font-size: 1.8rem !important;
  font-weight: 700 !important;
  margin: 1rem 0 !important;
}

p {
  font-family: 'Cormorant Garamond', serif !important;
  color: #e0e0e0 !important;
  font-size: 1.1rem !important;
  text-align: center !important;
}

/* Button styling */
button {
  background: linear-gradient(135deg, #d4af37 0%, #f0e68c 100%) !important;
  color: #1a1a2e !important;
  border: none !important;
  padding: 12px 28px !important;
  font-size: 1rem !important;
  font-weight: 700 !important;
  border-radius: 8px !important;
  cursor: pointer !important;
  transition: all 0.3s ease !important;
  font-family: 'Cormorant Garamond', serif !important;
  text-transform: uppercase !important;
  letter-spacing: 1px !important;
  margin: 8px !important;
  box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3) !important;
}

button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5) !important;
}

button:active {
  transform: translateY(0) !important;
}

/* Input styling */
input[type="text"], input[type="email"], textarea {
  background: rgba(255, 255, 255, 0.05) !important;
  color: #e0e0e0 !important;
  border: 2px solid #d4af37 !important;
  padding: 10px 15px !important;
  border-radius: 6px !important;
  font-family: 'Cormorant Garamond', serif !important;
  font-size: 1rem !important;
}

input[type="text"]:focus, input[type="email"]:focus, textarea:focus {
  outline: none !important;
  border-color: #f0e68c !important;
  box-shadow: 0 0 10px rgba(212, 175, 55, 0.3) !important;
}

/* Gallery styling */
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 12px;
  margin-top: 20px;
  padding: 20px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  border: 2px solid #d4af37;
}

.gallery-item {
  position: relative;
  overflow: hidden;
  border-radius: 6px;
  aspect-ratio: 9/16;
  border: 2px solid #d4af37;
  transition: all 0.3s ease;
}

.gallery-item:hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px rgba(212, 175, 55, 0.5);
}

.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Status messages */
.status-success {
  color: #4ade80 !important;
  font-weight: 700 !important;
}

.status-error {
  color: #f87171 !important;
  font-weight: 700 !important;
}

.status-info {
  color: #60a5fa !important;
  font-weight: 700 !important;
}

/* Overlay styling */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: none;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.overlay.open {
  display: flex;
}

.overlay-content {
  background: #1a1a2e;
  padding: 30px;
  border-radius: 12px;
  border: 2px solid #d4af37;
  max-width: 90vw;
  max-height: 90vh;
  overflow-y: auto;
}

/* Responsive */
@media (max-width: 768px) {
  h1 { font-size: 1.8rem !important; }
  h2 { font-size: 1.4rem !important; }
  p { font-size: 1rem !important; }
  button { padding: 10px 20px !important; font-size: 0.9rem !important; }
}
</style>
""", unsafe_allow_html=True)

# ── HTML/Canvas/Camera Interface ───────────────────────────────
if FRAME_OK:
    st_html(f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ margin: 0; padding: 20px; background: #0a0a0a; font-family: 'Cormorant Garamond', serif; }}
        .main-wrapper {{ 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center; 
            min-height: 100vh;
            gap: 20px;
        }}
        .title {{
            font-family: 'Playfair Display', serif;
            font-size: 2.2rem;
            font-weight: 900;
            color: #d4af37;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin: 0;
        }}
        .subtitle {{
            font-family: 'Playfair Display', serif;
            font-size: 1.4rem;
            color: #f0e68c;
            text-align: center;
            margin: 0;
        }}
        .controls {{
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
            margin: 15px 0;
        }}
        button {{
            background: linear-gradient(135deg, #d4af37 0%, #f0e68c 100%);
            color: #1a1a2e;
            border: none;
            padding: 12px 24px;
            font-size: 1rem;
            font-weight: 700;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Cormorant Garamond', serif;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
        }}
        button:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5); }}
        button:disabled {{ opacity: 0.5; cursor: not-allowed; }}
        .frame-wrapper {{
            position: relative;
            display: inline-block;
            max-width: 100%;
            width: 90vmin;
            max-width: 600px;
        }}
        #frameImg {{
            width: 100%;
            height: auto;
            display: block;
        }}
        canvas {{
            display: none;
        }}
        .status {{
            font-family: 'Cormorant Garamond', serif;
            font-size: 1.1rem;
            color: #e0e0e0;
            text-align: center;
            min-height: 30px;
        }}
        .status.success {{ color: #4ade80; font-weight: 700; }}
        .status.error {{ color: #f87171; font-weight: 700; }}
        .status.info {{ color: #60a5fa; font-weight: 700; }}
        .gallery-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }}
        .gallery-overlay.open {{
            display: flex;
        }}
        .gallery-content {{
            background: #1a1a2e;
            padding: 30px;
            border-radius: 12px;
            border: 2px solid #d4af37;
            max-width: 90vw;
            max-height: 90vh;
            overflow-y: auto;
        }}
        .gallery-title {{
            font-family: 'Playfair Display', serif;
            font-size: 1.8rem;
            color: #d4af37;
            text-align: center;
            margin-bottom: 20px;
        }}
        .gallery-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .gallery-item {{
            position: relative;
            overflow: hidden;
            border-radius: 6px;
            aspect-ratio: 9/16;
            border: 2px solid #d4af37;
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        .gallery-item:hover {{
            transform: scale(1.05);
            box-shadow: 0 0 15px rgba(212, 175, 55, 0.5);
        }}
        .gallery-item img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        .gallery-item-btn {{
            position: absolute;
            bottom: 5px;
            right: 5px;
            background: rgba(212, 175, 55, 0.9);
            color: #1a1a2e;
            border: none;
            padding: 6px 10px;
            border-radius: 4px;
            font-size: 0.8rem;
            cursor: pointer;
            opacity: 0;
            transition: opacity 0.3s;
        }}
        .gallery-item:hover .gallery-item-btn {{
            opacity: 1;
        }}
        .gallery-empty {{
            text-align: center;
            color: #999;
            padding: 40px;
            font-family: 'Cormorant Garamond', serif;
            font-size: 1.2rem;
        }}
        .gallery-controls {{
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
        }}
        input[type="file"] {{
            display: none;
        }}
        .file-label {{
            background: linear-gradient(135deg, #d4af37 0%, #f0e68c 100%);
            color: #1a1a2e;
            border: none;
            padding: 12px 24px;
            font-size: 1rem;
            font-weight: 700;
            border-radius: 6px;
            cursor: pointer;
            font-family: 'Cormorant Garamond', serif;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
            display: inline-block;
        }}
        .file-label:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5);
        }}
    </style>
    </head>
    <body>
    <div class="main-wrapper">
        <h1 class="title">✦ Apostle Victor A. Howard Sr. ✦</h1>
        <p class="subtitle">Birthday Celebration Photo Frame</p>
        
        <div class="controls">
            <button id="camBtn" onclick="toggleCamera()">📷 Camera</button>
            <label class="file-label" for="fi">📁 Upload</label>
            <input type="file" id="fi" accept="image/*">
            <button id="galBtn" onclick="openGal()" style="display:none;">🖼 Gallery (<span id="galCount">0</span>)</button>
        </div>
        
        <div class="status" id="status">Ready to capture your photo</div>
        
        <div class="frame-wrapper">
            <img id="frameImg" src="data:image/png;base64,{frame_b64}" alt="Frame">
            <canvas id="liveC"></canvas>
            <canvas id="snapC"></canvas>
            <canvas id="upC"></canvas>
        </div>
        
        <div class="controls" id="camControls" style="display:none;">
            <button id="snapBtn" onclick="doSnap()">📸 Capture</button>
            <button id="flipBtn" onclick="flipCam()">🔄 Flip</button>
            <button id="retakeBtn" onclick="doRetake()" hidden>🔁 Retake</button>
        </div>
    </div>
    
    <div class="gallery-overlay" id="galOverlay">
        <div class="gallery-content">
            <h2 class="gallery-title">✦ Your Photos ✦</h2>
            <div class="gallery-grid" id="galGrid"></div>
            <div class="gallery-empty" id="galEmpty">No photos yet</div>
            <div class="gallery-controls">
                <button onclick="closeGal()">Close</button>
                <button onclick="clearGal()" style="background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);">Clear All</button>
            </div>
        </div>
    </div>
    
    <script>
    const frameImg = document.getElementById('frameImg');
    const liveC = document.getElementById('liveC');
    const snapC = document.getElementById('snapC');
    const upC = document.getElementById('upC');
    const status = document.getElementById('status');
    const camBtn = document.getElementById('camBtn');
    const camControls = document.getElementById('camControls');
    const galBtn = document.getElementById('galBtn');
    
    let vid, animId = null, snapped = false, facing = 'environment';
    const gallery = [];
    
    function getFW() {{ return frameImg.naturalWidth || 600; }}
    function getFH() {{ return frameImg.naturalHeight || 1067; }}
    
    function composite(src, canvas) {{
        const FW = getFW(), FH = getFH();
        const ctx = canvas.getContext('2d');
        canvas.width = FW;
        canvas.height = FH;
        
        // Cutout coordinates for Apostle Victor frame
        const cutoutTop = 375, cutoutBottom = 1243, cutoutLeft = 234, cutoutRight = 627;
        const cutoutW = cutoutRight - cutoutLeft, cutoutH = cutoutBottom - cutoutTop;
        
        // Get source dimensions
        const srcW = src.videoWidth || src.naturalWidth || src.width;
        const srcH = src.videoHeight || src.naturalHeight || src.height;
        const srcAspect = srcW / srcH;
        const cutoutAspect = cutoutW / cutoutH;
        
        // Calculate crop
        let sx, sy, sw, sh;
        if (srcAspect > cutoutAspect) {{
            sw = srcH * cutoutAspect;
            sh = srcH;
            sx = (srcW - sw) / 2;
            sy = 0;
        }} else {{
            sw = srcW;
            sh = srcW / cutoutAspect;
            sx = 0;
            sy = (srcH - sh) / 2;
        }}
        
        // Draw cropped source to cutout area
        ctx.drawImage(src, sx, sy, sw, sh, cutoutLeft, cutoutTop, cutoutW, cutoutH);
        
        // Composite frame on top
        ctx.drawImage(frameImg, 0, 0, FW, FH);
    }}
    
    function toggleCamera() {{
        if (vid && vid.srcObject) {{
            vid.srcObject.getTracks().forEach(t => t.stop());
            vid = null;
            camBtn.textContent = '📷 Camera';
            camControls.style.display = 'none';
            snapped = false;
            liveC.style.display = 'none';
            snapC.style.display = 'none';
            status.textContent = 'Camera closed';
            status.className = 'status info';
        }} else {{
            startCamera(facing);
        }}
    }}
    
    function startCamera(f) {{
        facing = f;
        status.textContent = 'Requesting camera access...';
        status.className = 'status info';
        navigator.mediaDevices.getUserMedia({{ video: {{ facingMode: facing }} }})
            .then(stream => {{
                vid = document.createElement('video');
                vid.srcObject = stream;
                vid.play();
                camBtn.textContent = '📷 Close Camera';
                camControls.style.display = 'flex';
                status.textContent = facing === 'environment' ? '📷 Rear camera — aim & capture' : '🤳 Front camera active';
                status.className = 'status info';
                snapped = false;
                liveC.style.display = 'block';
                snapC.style.display = 'none';
                document.getElementById('snapBtn').hidden = false;
                document.getElementById('flipBtn').hidden = false;
                document.getElementById('retakeBtn').hidden = true;
                startLive();
            }})
            .catch(e => {{
                status.textContent = '⚠ ' + e.message;
                status.className = 'status error';
            }});
    }}
    
    function startLive() {{
        if (animId) cancelAnimationFrame(animId);
        function draw() {{
            if (snapped) return;
            animId = requestAnimationFrame(draw);
            if (!vid.videoWidth || !vid.videoHeight || !frameImg.complete) return;
            composite(vid, liveC);
        }}
        draw();
    }}
    
    function doSnap() {{
        if (!vid.videoWidth) return;
        snapped = true;
        if (animId) cancelAnimationFrame(animId);
        composite(vid, snapC);
        liveC.style.display = 'none';
        snapC.style.display = 'block';
        document.getElementById('snapBtn').hidden = true;
        document.getElementById('flipBtn').hidden = true;
        document.getElementById('retakeBtn').hidden = false;
        status.textContent = '✅ Photo captured!';
        status.className = 'status success';
        
        // Add to gallery
        addGallery(snapC);
    }}
    
    function doRetake() {{
        snapped = false;
        liveC.style.display = 'block';
        snapC.style.display = 'none';
        document.getElementById('snapBtn').hidden = false;
        document.getElementById('flipBtn').hidden = false;
        document.getElementById('retakeBtn').hidden = true;
        status.textContent = '📷 Ready — aim and capture';
        status.className = 'status info';
        startLive();
    }}
    
    function flipCam() {{
        facing = facing === 'environment' ? 'user' : 'environment';
        if (vid && vid.srcObject) {{
            vid.srcObject.getTracks().forEach(t => t.stop());
        }}
        startCamera(facing);
    }}
    
    // Upload handler
    document.getElementById('fi').addEventListener('change', e => {{
        const file = e.target.files[0];
        if (!file) return;
        status.textContent = 'Processing…';
        status.className = 'status info';
        const reader = new FileReader();
        reader.onload = ev => {{
            const img = new Image();
            img.onload = () => {{
                function go() {{
                    composite(img, upC);
                    upC.style.display = 'block';
                    status.textContent = '✅ Photo framed — save to gallery!';
                    status.className = 'status success';
                    addGallery(upC);
                }}
                if (frameImg.complete && frameImg.naturalWidth) go();
                else frameImg.onload = go;
            }};
            img.src = ev.target.result;
        }};
        reader.readAsDataURL(file);
    }});
    
    // Gallery functions
    function addGallery(canvas) {{
        canvas.toBlob(blob => {{
            const url = URL.createObjectURL(blob);
            gallery.unshift(url);
            renderGal();
            galBtn.style.display = 'inline-block';
            document.getElementById('galCount').textContent = gallery.length;
        }}, 'image/png');
    }}
    
    function renderGal() {{
        const grid = document.getElementById('galGrid');
        const empty = document.getElementById('galEmpty');
        grid.innerHTML = '';
        empty.style.display = gallery.length ? 'none' : 'block';
        gallery.forEach((url, i) => {{
            const wrap = document.createElement('div');
            wrap.className = 'gallery-item';
            const img = document.createElement('img');
            img.src = url;
            const btn = document.createElement('button');
            btn.className = 'gallery-item-btn';
            btn.textContent = '⬇ Save';
            btn.onclick = e => {{
                e.stopPropagation();
                const a = document.createElement('a');
                a.href = url;
                a.download = `apostle_victor_${{i + 1}}.png`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            }};
            wrap.appendChild(img);
            wrap.appendChild(btn);
            grid.appendChild(wrap);
        }});
    }}
    
    function openGal() {{
        renderGal();
        document.getElementById('galOverlay').classList.add('open');
    }}
    
    function closeGal() {{
        document.getElementById('galOverlay').classList.remove('open');
    }}
    
    function clearGal() {{
        if (confirm('Clear all photos?')) {{
            gallery.length = 0;
            renderGal();
            galBtn.style.display = 'none';
            document.getElementById('galCount').textContent = '0';
            status.textContent = 'Gallery cleared';
            status.className = 'status info';
        }}
    }}
    
    // Sync height
    function syncH() {{
        try {{
            window.parent.postMessage({{type: 'streamlit:setFrameHeight', height: document.body.scrollHeight}}, '*');
        }} catch (e) {{}}
    }}
    setInterval(syncH, 800);
    </script>
    </body>
    </html>
    """, height=1200)

# ── Error State ────────────────────────────────────────────────
if not FRAME_OK:
    st.error(
        "⚠️ **apostle_victor_frame.png not found.**  "
        "Place the frame image in the same folder as `app.py`, then refresh.",
        icon="🖼",
    )
