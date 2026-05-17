import streamlit as st
from PIL import Image
import os, base64
from streamlit.components.v1 import html as st_html

st.set_page_config(
    page_title="🎉 Elease Benford – 80th Birthday",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit chrome
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main { background:#062918 !important; }
[data-testid="stHeader"] { background:transparent !important; }
[data-testid="stMainBlockContainer"] { padding:0 !important; }
#MainMenu, footer, header { visibility:hidden; }
.block-container { padding:0 !important; max-width:100% !important; }
</style>
""", unsafe_allow_html=True)

# Load frame as base64
FRAME_PATH = os.path.join(os.path.dirname(__file__), "frame.png")
with open(FRAME_PATH, "rb") as f:
    FRAME_B64 = base64.b64encode(f.read()).decode()

# Cutout in the frame image (pixels at full resolution)
CUT = dict(top=106, bottom=961, left=269, right=785)

# Build the single-page component
APP_HTML = f"""<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Cormorant+Garamond:ital,wght@0,400;1,300&display=swap" rel="stylesheet">
<style>
:root {{
  --gold:  #c9a84c;
  --gold2: #ffe066;
  --bg:    #062918;
  --bg2:   #0d3d20;
}}
* {{ margin:0; padding:0; box-sizing:border-box; -webkit-tap-highlight-color:transparent; }}
html, body {{ background:var(--bg); font-family:'Cinzel',serif; color:var(--gold); overflow-x:hidden; }}

/* ── HEADER ── */
.hdr {{ text-align:center; padding:18px 16px 10px; }}
.hdr h1 {{
  font-size:clamp(1.3rem,5vw,2rem); font-weight:900; color:var(--gold2);
  letter-spacing:.12em; text-shadow:0 0 30px rgba(255,224,102,.5); line-height:1.2;
}}
.hdr .sub {{
  font-family:'Cormorant Garamond',serif; font-style:italic;
  font-size:clamp(.85rem,3vw,1rem); color:rgba(201,168,76,.65);
  letter-spacing:.06em; margin-top:4px;
}}
.divider {{
  height:1px; background:linear-gradient(90deg,transparent,var(--gold),transparent);
  opacity:.45; margin:10px 16px;
}}

/* ── TABS ── */
.tabs {{ display:flex; border-bottom:1px solid rgba(201,168,76,.2); margin:0 12px 10px; }}
.tab {{
  flex:1; padding:9px 4px; text-align:center;
  font-size:.72rem; letter-spacing:.12em; text-transform:uppercase;
  color:rgba(201,168,76,.4); cursor:pointer; border-bottom:2px solid transparent;
  transition:all .2s;
}}
.tab.active {{ color:var(--gold2); border-bottom-color:var(--gold); background:rgba(201,168,76,.05); }}

/* ── PANELS ── */
.panel {{ display:none; padding:0 12px; }}
.panel.active {{ display:block; }}

/* ── CAMERA CANVAS WRAP ── */
#camWrap {{
  position:relative; width:100%; border-radius:8px; overflow:hidden;
  box-shadow:0 6px 32px rgba(0,0,0,.7);
}}
#liveCanvas, #snapCanvas {{
  width:100%; display:block; border-radius:8px;
}}
#snapCanvas {{ display:none; }}

/* ── UPLOAD PREVIEW ── */
#uploadPreview {{
  width:100%; border-radius:8px; display:none;
  box-shadow:0 6px 32px rgba(0,0,0,.7);
}}

/* ── BIG STATUS BAR ── */
#status {{
  text-align:center; font-size:.68rem; letter-spacing:.1em;
  color:rgba(201,168,76,.5); min-height:1.4em; margin:8px 0 4px;
}}

/* ── BUTTONS ── */
.btnrow {{ display:flex; gap:8px; margin:8px 0; }}
.btn {{
  flex:1; padding:13px 6px; border:none; border-radius:5px; cursor:pointer;
  font-family:'Cinzel',serif; font-weight:700; font-size:.8rem;
  letter-spacing:.09em; text-transform:uppercase;
  transition:opacity .15s, box-shadow .2s;
}}
.btn:active {{ opacity:.7; }}
.btn.gold {{
  background:linear-gradient(135deg,#7a5c10,#e8c05a,#7a5c10); color:var(--bg);
  box-shadow:0 4px 20px rgba(201,168,76,.45); flex:2;
}}
.btn.gold:hover {{ box-shadow:0 8px 32px rgba(201,168,76,.7); }}
.btn.outline {{
  background:rgba(201,168,76,.08); border:1px solid rgba(201,168,76,.35);
  color:rgba(201,168,76,.8); flex:1;
}}
.btn.danger {{
  background:rgba(180,40,40,.15); border:1px solid rgba(200,60,60,.35);
  color:rgba(220,100,100,.8); flex:1;
}}

/* ── UPLOAD AREA ── */
#dropZone {{
  border:2px dashed rgba(201,168,76,.4); border-radius:8px;
  padding:32px 16px; text-align:center; cursor:pointer;
  background:var(--bg2); margin-bottom:8px; transition:border-color .2s;
}}
#dropZone:hover {{ border-color:var(--gold); }}
#dropZone p {{ font-size:.78rem; letter-spacing:.1em; color:rgba(201,168,76,.55); margin-bottom:6px; }}
#dropZone small {{ font-size:.65rem; color:rgba(201,168,76,.3); letter-spacing:.08em; }}
#fileInput {{ display:none; }}

/* ── GALLERY ── */
#gallerySection {{ margin-top:12px; }}
.gal-label {{
  font-size:.65rem; letter-spacing:.18em; text-transform:uppercase;
  color:rgba(201,168,76,.35); margin-bottom:8px;
}}
.gal-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:6px; }}
.gal-item {{ position:relative; cursor:pointer; }}
.gal-item img {{ width:100%; border-radius:4px; display:block; }}
.gal-item .dl-btn {{
  position:absolute; bottom:0; left:0; right:0;
  background:rgba(6,41,24,.82); color:var(--gold2);
  font-size:.58rem; letter-spacing:.08em; text-align:center;
  padding:5px 2px; border-radius:0 0 4px 4px;
  opacity:0; transition:opacity .2s; cursor:pointer;
  font-family:'Cinzel',serif; font-weight:700; text-transform:uppercase;
  border:none; width:100%;
}}
.gal-item:hover .dl-btn {{ opacity:1; }}

/* ── FOOTER ── */
.ftr {{
  text-align:center; padding:20px 16px 30px;
  font-family:'Cormorant Garamond',serif; font-style:italic;
  font-size:.9rem; color:rgba(201,168,76,.3); letter-spacing:.05em;
}}

/* ── SPARKLES ── */
#spbg {{ position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;overflow:hidden; }}
.page-content {{ position:relative; z-index:1; }}
</style>
</head>
<body>

<div id="spbg"></div>

<div class="page-content">

  <!-- HEADER -->
  <div class="hdr">
    <h1>✦ 80th Birthday Frame ✦</h1>
    <div class="sub">Elease Benford &nbsp;·&nbsp; Eighty Magnificent Years</div>
  </div>
  <div class="divider"></div>

  <!-- TABS -->
  <div class="tabs">
    <div class="tab active" id="tabCam" onclick="switchTab('cam')">📷 &nbsp;Live Camera</div>
    <div class="tab" id="tabUp"  onclick="switchTab('up')">🖼 &nbsp;Upload Photo</div>
  </div>

  <!-- CAMERA PANEL -->
  <div class="panel active" id="panelCam">
    <div id="camWrap">
      <canvas id="liveCanvas"></canvas>
      <canvas id="snapCanvas"></canvas>
    </div>
    <div id="status">Starting rear camera…</div>
    <div class="btnrow" id="camBtns">
      <button class="btn outline" id="flipBtn"   onclick="flipCam()">🔁 Flip</button>
      <button class="btn gold"   id="snapBtn"   onclick="doSnap()">📸 CAPTURE</button>
      <button class="btn outline" id="retakeBtn" onclick="doRetake()" style="display:none">🔄 Retake</button>
    </div>
    <!-- Download + gallery save appear after snap -->
    <div id="afterSnap" style="display:none">
      <div class="btnrow">
        <button class="btn gold"    id="dlBtn"  onclick="downloadSnap()">⬇ Download</button>
        <button class="btn outline" id="saveBtn" onclick="saveToGallery()">➕ Gallery</button>
      </div>
    </div>
  </div>

  <!-- UPLOAD PANEL -->
  <div class="panel" id="panelUp">
    <div id="dropZone" onclick="document.getElementById('fileInput').click()">
      <p>Tap to choose a photo</p>
      <small>JPG · PNG · HEIC</small>
    </div>
    <input type="file" id="fileInput" accept="image/*" onchange="handleUpload(event)">
    <canvas id="uploadCanvas" style="width:100%;border-radius:8px;display:none;box-shadow:0 6px 32px rgba(0,0,0,.7)"></canvas>
    <div id="upStatus" style="text-align:center;font-size:.68rem;letter-spacing:.1em;color:rgba(201,168,76,.5);min-height:1.4em;margin:8px 0 4px;"></div>
    <div id="afterUpload" style="display:none">
      <div class="btnrow">
        <button class="btn gold"    onclick="downloadUpload()">⬇ Download</button>
        <button class="btn outline" onclick="saveUploadToGallery()">➕ Gallery</button>
      </div>
    </div>
  </div>

  <div class="divider"></div>

  <!-- GALLERY -->
  <div id="gallerySection" style="padding:0 12px; display:none">
    <div class="gal-label">✦ &nbsp; Gallery &nbsp; ✦</div>
    <div class="gal-grid" id="galGrid"></div>
    <div class="btnrow" style="margin-top:10px">
      <button class="btn danger" onclick="clearGallery()">🗑 Clear Gallery</button>
    </div>
    <div class="divider" style="margin-top:12px"></div>
  </div>

  <!-- FOOTER -->
  <div class="ftr">🌿 &nbsp; Eighty years of love, grace, wisdom &amp; joy &nbsp; 🌿</div>

</div><!-- end page-content -->

<!-- Hidden video -->
<video id="vid" autoplay playsinline muted style="display:none;position:absolute;width:1px;height:1px"></video>

<script>
// ══════════════════════════════════════════════════════════════
// SPARKLES
// ══════════════════════════════════════════════════════════════
(function(){{
  const bg = document.getElementById('spbg');
  const s = document.createElement('style');
  s.textContent = '@keyframes tw{{0%,100%{{opacity:0;transform:scale(.3)}}50%{{opacity:.5;transform:scale(1.4)}}}}';
  document.head.appendChild(s);
  for (let i=0;i<80;i++) {{
    const d = document.createElement('div');
    const sz = Math.random()*3+1;
    d.style.cssText = `position:absolute;border-radius:50%;background:#ffe066;width:${{sz}}px;height:${{sz}}px;`
      +`left:${{Math.random()*100}}%;top:${{Math.random()*100}}%;opacity:0;`
      +`animation:tw ${{2.5+Math.random()*4}}s ease-in-out ${{-Math.random()*6}}s infinite;`;
    bg.appendChild(d);
  }}
}})();

// ══════════════════════════════════════════════════════════════
// FRAME  (loaded once, used by both camera & upload paths)
// ══════════════════════════════════════════════════════════════
const FRAME_SRC = 'data:image/png;base64,{FRAME_B64}';
const CUT = {{ top:{CUT['top']}, bottom:{CUT['bottom']}, left:{CUT['left']}, right:{CUT['right']} }};
const CUT_W = CUT.right - CUT.left;
const CUT_H = CUT.bottom - CUT.top;
const CUT_R = CUT_W / CUT_H;

const frameImg = new Image();
frameImg.src   = FRAME_SRC;

// ══════════════════════════════════════════════════════════════
// TABS
// ══════════════════════════════════════════════════════════════
function switchTab(t) {{
  document.querySelectorAll('.tab').forEach(e => e.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(e => e.classList.remove('active'));
  document.getElementById('tab' + (t==='cam'?'Cam':'Up')).classList.add('active');
  document.getElementById('panel' + (t==='cam'?'Cam':'Up')).classList.add('active');
  if (t === 'cam' && !stream) startCamera('environment');
}}

// ══════════════════════════════════════════════════════════════
// CAMERA
// ══════════════════════════════════════════════════════════════
const vid      = document.getElementById('vid');
const liveC    = document.getElementById('liveCanvas');
const snapC    = document.getElementById('snapCanvas');
const liveCtx  = liveC.getContext('2d');
const snapCtx  = snapC.getContext('2d');
const status   = document.getElementById('status');
const snapBtn  = document.getElementById('snapBtn');
const retakeBtn= document.getElementById('retakeBtn');
const flipBtn  = document.getElementById('flipBtn');
const afterSnap= document.getElementById('afterSnap');

let stream = null, facing = 'environment', animId = null, snapped = false;
let snapDataUrl = null;

// Helper: crop source to CUT_R aspect ratio, centre-crop
function cropArgs(vw, vh) {{
  let sx, sy, sw, sh;
  if (vw/vh > CUT_R) {{
    sh=vh; sw=Math.round(vh*CUT_R); sx=Math.round((vw-sw)/2); sy=0;
  }} else {{
    sw=vw; sh=Math.round(vw/CUT_R); sx=0; sy=Math.round((vh-sh)/2);
  }}
  return {{sx,sy,sw,sh}};
}}

async function startCamera(f) {{
  if (stream) stream.getTracks().forEach(t=>t.stop());
  status.textContent = 'Starting ' + (f==='environment'?'rear':'front') + ' camera…';
  try {{
    stream = await navigator.mediaDevices.getUserMedia({{
      video:{{ facingMode:{{ideal:f}}, width:{{ideal:1920}}, height:{{ideal:1080}} }},
      audio:false
    }});
    vid.srcObject = stream;
    await new Promise(r => vid.onloadedmetadata = r);
    await vid.play();
    const s = stream.getVideoTracks()[0].getSettings();
    facing = s.facingMode || f;
    status.textContent = facing==='environment' ? '📷 Rear camera — point & capture' : '🤳 Front camera active';
    if (!snapped) startLive();
  }} catch(e) {{
    status.textContent = '⚠ ' + e.message;
  }}
}}

function getFW() {{ return frameImg.naturalWidth  || 1054; }}
function getFH() {{ return frameImg.naturalHeight || 1067; }}

function startLive() {{
  if (animId) cancelAnimationFrame(animId);
  function draw() {{
    if (snapped) return;
    animId = requestAnimationFrame(draw);
    const vw=vid.videoWidth, vh=vid.videoHeight;
    if (!vw || !vh || !frameImg.complete) return;
    const FW=getFW(), FH=getFH();
    if (liveC.width!==FW) {{ liveC.width=FW; liveC.height=FH; }}
    const {{sx,sy,sw,sh}} = cropArgs(vw,vh);
    liveCtx.drawImage(vid, sx,sy,sw,sh, CUT.left,CUT.top,CUT_W,CUT_H);
    liveCtx.drawImage(frameImg, 0,0,FW,FH);
  }}
  draw();
}}

function doSnap() {{
  if (!vid.videoWidth) return;
  snapped=true;
  if (animId) cancelAnimationFrame(animId);
  const FW=getFW(), FH=getFH();
  snapC.width=FW; snapC.height=FH;
  const vw=vid.videoWidth, vh=vid.videoHeight;
  const {{sx,sy,sw,sh}} = cropArgs(vw,vh);
  snapCtx.drawImage(vid, sx,sy,sw,sh, CUT.left,CUT.top,CUT_W,CUT_H);
  snapCtx.drawImage(frameImg, 0,0,FW,FH);
  snapDataUrl = snapC.toDataURL('image/png');

  liveC.style.display='none';
  snapC.style.display='block';
  snapBtn.style.display='none';
  flipBtn.style.display='none';
  retakeBtn.style.display='flex';
  afterSnap.style.display='block';
  status.textContent = '✅ Photo captured!';
}}

function doRetake() {{
  snapped=false; snapDataUrl=null;
  liveC.style.display='block';
  snapC.style.display='none';
  snapBtn.style.display='flex';
  flipBtn.style.display='flex';
  retakeBtn.style.display='none';
  afterSnap.style.display='none';
  status.textContent = '📷 Ready — aim and capture';
  startLive();
}}

function flipCam() {{
  facing = facing==='environment'?'user':'environment';
  startCamera(facing);
}}

function downloadSnap() {{
  if (!snapDataUrl) return;
  const a = document.createElement('a');
  a.href = snapDataUrl;
  a.download = 'elease_80th_birthday.png';
  a.click();
}}

// ══════════════════════════════════════════════════════════════
// GALLERY  (stored in memory as data URLs)
// ══════════════════════════════════════════════════════════════
const gallery = [];

function renderGallery() {{
  const sec  = document.getElementById('gallerySection');
  const grid = document.getElementById('galGrid');
  if (gallery.length===0) {{ sec.style.display='none'; return; }}
  sec.style.display='block';
  grid.innerHTML = '';
  gallery.forEach((url, i) => {{
    const item = document.createElement('div');
    item.className = 'gal-item';
    const img = document.createElement('img');
    img.src = url;
    const btn = document.createElement('button');
    btn.className = 'dl-btn';
    btn.textContent = '⬇ Save';
    btn.onclick = () => {{ const a=document.createElement('a'); a.href=url; a.download=`elease_80th_${{i+1}}.png`; a.click(); }};
    item.appendChild(img);
    item.appendChild(btn);
    grid.appendChild(item);
  }});
}}

function saveToGallery() {{
  if (!snapDataUrl) return;
  gallery.unshift(snapDataUrl);
  renderGallery();
  status.textContent = '✅ Saved to gallery!';
  setTimeout(()=>{{ status.textContent='📷 Tap Retake to take another photo'; }}, 1800);
}}

function clearGallery() {{
  gallery.length = 0;
  renderGallery();
}}

// ══════════════════════════════════════════════════════════════
// UPLOAD PATH
// ══════════════════════════════════════════════════════════════
let uploadDataUrl = null;
const uploadCanvas = document.getElementById('uploadCanvas');
const uploadCtx    = uploadCanvas.getContext('2d');
const upStatus     = document.getElementById('upStatus');
const afterUpload  = document.getElementById('afterUpload');

function handleUpload(e) {{
  const file = e.target.files[0];
  if (!file) return;
  upStatus.textContent = 'Processing…';
  const reader = new FileReader();
  reader.onload = ev => {{
    const img = new Image();
    img.onload = () => {{
      // Wait for frame
      function composite() {{
        const FW=getFW(), FH=getFH();
        uploadCanvas.width=FW; uploadCanvas.height=FH;
        const vw=img.naturalWidth, vh=img.naturalHeight;
        const {{sx,sy,sw,sh}} = cropArgs(vw,vh);
        uploadCtx.drawImage(img, sx,sy,sw,sh, CUT.left,CUT.top,CUT_W,CUT_H);
        uploadCtx.drawImage(frameImg, 0,0,FW,FH);
        uploadCanvas.style.display='block';
        uploadDataUrl = uploadCanvas.toDataURL('image/png');
        upStatus.textContent = '✅ Photo framed!';
        afterUpload.style.display='block';
      }}
      if (frameImg.complete && frameImg.naturalWidth) composite();
      else {{ frameImg.onload = composite; }}
    }};
    img.src = ev.target.result;
  }};
  reader.readAsDataURL(file);
}}

function downloadUpload() {{
  if (!uploadDataUrl) return;
  const a = document.createElement('a');
  a.href = uploadDataUrl;
  a.download = 'elease_80th_birthday.png';
  a.click();
}}

function saveUploadToGallery() {{
  if (!uploadDataUrl) return;
  gallery.unshift(uploadDataUrl);
  renderGallery();
  upStatus.textContent = '✅ Saved to gallery!';
}}

// ══════════════════════════════════════════════════════════════
// BOOT
// ══════════════════════════════════════════════════════════════
frameImg.onload = () => startCamera('environment');
if (frameImg.complete && frameImg.naturalWidth) startCamera('environment');

// Tell Streamlit iframe height
function setH() {{
  try {{
    Streamlit.setFrameHeight(document.body.scrollHeight + 20);
  }} catch(e) {{}}
}}
setInterval(setH, 600);
window.addEventListener('resize', setH);
</script>
</body>
</html>"""

st_html(APP_HTML, height=1200, scrolling=True)
