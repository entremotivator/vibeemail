import streamlit as st
from PIL import Image
import io, os, base64
from streamlit.components.v1 import html as st_html

st.set_page_config(
    page_title="✦ Elease Benford – 80th Birthday",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Global CSS: kill all Streamlit chrome, fix viewport ───────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,400&family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&display=swap');

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main,
[data-testid="stMainBlockContainer"],
section[data-testid="stMain"] {
    background: #071e12 !important;
    overflow: hidden !important;
    height: 100vh !important;
    max-height: 100vh !important;
}
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display:none !important; }
#MainMenu, footer, header { visibility:hidden !important; }
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
    height: 100vh !important;
    overflow: hidden !important;
}
/* Hide Streamlit download button default styling — we'll style via JS injected into iframe */
[data-testid="stDownloadButton"] > button {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ── Load frame.png ────────────────────────────────────────────
FRAME_PATH = os.path.join(os.path.dirname(__file__), "frame.png")
try:
    with open(FRAME_PATH, "rb") as f:
        FRAME_B64 = base64.b64encode(f.read()).decode()
    FRAME_OK = True
except FileNotFoundError:
    FRAME_B64 = ""
    FRAME_OK = False

# Cutout rectangle inside frame.png (pixels at natural resolution)
CUT = dict(top=106, bottom=961, left=269, right=785)

# ── Build the full-viewport single-page component ─────────────
APP_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Cormorant+Garamond:ital,wght@0,300;1,300&display=swap" rel="stylesheet">
<style>
:root {{
  --gold:  #c9a84c;
  --gold2: #f0d080;
  --gold3: #ffe8a0;
  --bg:    #071e12;
  --bg2:   #0b2c19;
  --bg3:   #0f3820;
  --dim:   rgba(201,168,76,.45);
  --faint: rgba(201,168,76,.22);
}}
*,*::before,*::after{{ margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent; }}
html,body{{
  width:100%;height:100vh;overflow:hidden;
  background:var(--bg);
  font-family:'Playfair Display',serif;
  color:var(--gold);
}}

/* SPARKLES */
#sp{{position:fixed;inset:0;pointer-events:none;z-index:0;overflow:hidden;}}
@keyframes tw{{0%,100%{{opacity:0;transform:scale(.2)}}50%{{opacity:.4;transform:scale(1.4)}}}}

/* SHELL */
.shell{{
  position:relative;z-index:1;
  width:100%;height:100vh;
  display:grid;
  grid-template-rows:auto auto 1fr auto auto;
  overflow:hidden;
}}

/* HEADER */
header{{
  text-align:center;padding:12px 18px 8px;
  border-bottom:1px solid var(--faint);
  background:rgba(7,30,18,.97);
}}
header h1{{
  font-size:clamp(1.05rem,3.8vw,1.65rem);font-weight:900;
  color:var(--gold3);letter-spacing:.14em;
  text-shadow:0 0 24px rgba(255,232,160,.3);line-height:1.15;
}}
header .sub{{
  font-family:'Cormorant Garamond',serif;font-style:italic;
  font-size:clamp(.74rem,1.9vw,.88rem);
  color:rgba(201,168,76,.5);letter-spacing:.08em;margin-top:2px;
}}

/* TABS */
.tabs{{display:flex;border-bottom:1px solid var(--faint);background:var(--bg2);}}
.tab{{
  flex:1;padding:9px 4px;text-align:center;
  font-size:.65rem;letter-spacing:.14em;text-transform:uppercase;
  color:rgba(201,168,76,.4);cursor:pointer;
  border-bottom:2px solid transparent;transition:all .2s;
  font-family:'Playfair Display',serif;font-weight:700;
}}
.tab.active{{color:var(--gold2);border-bottom-color:var(--gold);background:rgba(201,168,76,.06);}}

/* PANELS */
.panels{{position:relative;overflow:hidden;min-height:0;}}
.panel{{
  position:absolute;inset:0;
  display:flex;flex-direction:column;gap:7px;
  padding:10px 14px;
  opacity:0;pointer-events:none;transition:opacity .18s;
  overflow:hidden;
}}
.panel.active{{opacity:1;pointer-events:all;}}

/* CANVAS WRAP */
.cvs-wrap{{
  flex:1;min-height:0;position:relative;
  border-radius:8px;overflow:hidden;
  border:1px solid var(--faint);
  background:var(--bg3);
  display:flex;align-items:center;justify-content:center;
}}
.cvs-wrap canvas{{
  position:absolute;inset:0;width:100%;height:100%;object-fit:contain;
}}
.cvs-placeholder{{
  font-family:'Cormorant Garamond',serif;font-style:italic;
  color:rgba(201,168,76,.38);font-size:.84rem;letter-spacing:.08em;text-align:center;padding:16px;
}}

/* STATUS */
.status{{
  text-align:center;font-size:.62rem;letter-spacing:.12em;
  color:rgba(201,168,76,.45);
  font-family:'Cormorant Garamond',serif;font-style:italic;
  min-height:1em;flex-shrink:0;
}}

/* BUTTONS */
.btnrow{{display:flex;gap:7px;flex-shrink:0;}}
.btn{{
  flex:1;padding:11px 5px;border:none;border-radius:5px;cursor:pointer;
  font-family:'Playfair Display',serif;font-weight:700;
  font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;
  transition:opacity .15s;
}}
.btn:active{{opacity:.7;transform:scale(.98);}}
.btn.gold{{
  background:linear-gradient(135deg,#6b4e0e,#d4a83e,#8a6318,#e0ba55,#7a5c10);
  color:#0b1a0e;box-shadow:0 3px 14px rgba(201,168,76,.38);flex:2;
}}
.btn.outline{{
  background:rgba(201,168,76,.07);
  border:1px solid rgba(201,168,76,.4);color:rgba(201,168,76,.75);
}}
.btn.danger{{
  background:rgba(160,35,35,.1);
  border:1px solid rgba(190,60,60,.3);color:rgba(210,100,100,.8);
}}
.btn[hidden]{{display:none!important;}}

/* DROP ZONE */
.drop{{
  border:2px dashed rgba(201,168,76,.28);border-radius:8px;
  padding:18px 12px;text-align:center;cursor:pointer;
  background:var(--bg2);transition:border-color .2s;flex-shrink:0;
}}
.drop:hover{{border-color:var(--gold);}}
.drop p{{
  font-size:.76rem;letter-spacing:.1em;color:rgba(201,168,76,.45);
  margin-bottom:3px;font-family:'Cormorant Garamond',serif;font-style:italic;
}}
.drop small{{font-size:.6rem;color:rgba(201,168,76,.25);letter-spacing:.07em;font-family:'Cormorant Garamond',serif;}}

/* DOWNLOAD BAR */
#dlBar{{
  display:none;
  background:rgba(11,44,25,.96);
  border-top:1px solid var(--faint);
  padding:9px 14px;flex-shrink:0;
}}
#dlBar.show{{display:block;}}
#dlBar .inner{{display:flex;gap:8px;align-items:center;}}
#dlBar .info{{
  flex:1;font-size:.62rem;letter-spacing:.1em;
  color:rgba(201,168,76,.5);font-family:'Cormorant Garamond',serif;font-style:italic;
}}

/* GALLERY OVERLAY */
#galOverlay{{
  position:fixed;inset:0;z-index:200;
  background:rgba(4,12,7,.95);
  display:none;flex-direction:column;padding:14px;
  overflow-y:auto;
}}
#galOverlay.open{{display:flex;}}
.gal-head{{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;}}
.gal-title{{font-size:.78rem;letter-spacing:.18em;text-transform:uppercase;color:var(--gold2);}}
.gal-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;}}
.gal-item{{position:relative;border-radius:6px;overflow:hidden;cursor:pointer;}}
.gal-item img{{width:100%;display:block;}}
.gal-item .gal-dl{{
  position:absolute;bottom:0;left:0;right:0;
  background:rgba(4,12,7,.88);color:var(--gold2);
  font-size:.55rem;letter-spacing:.08em;text-align:center;padding:5px 2px;
  font-family:'Playfair Display',serif;font-weight:700;text-transform:uppercase;
  border:none;width:100%;cursor:pointer;opacity:0;transition:opacity .18s;
}}
.gal-item:hover .gal-dl{{opacity:1;}}
.gal-empty{{
  text-align:center;color:rgba(201,168,76,.35);
  font-family:'Cormorant Garamond',serif;font-style:italic;font-size:.84rem;
  margin:40px auto;
}}

/* FOOTER */
footer{{
  text-align:center;padding:7px 16px;
  font-family:'Cormorant Garamond',serif;font-style:italic;
  font-size:.74rem;color:rgba(201,168,76,.25);letter-spacing:.06em;
  border-top:1px solid var(--faint);background:rgba(7,30,18,.97);flex-shrink:0;
}}
</style>
</head>
<body>

<div id="sp"></div>

<div class="shell">

  <header>
    <h1>✦ &nbsp;80th Birthday Frame&nbsp; ✦</h1>
    <div class="sub">Elease Benford &nbsp;·&nbsp; Eighty Magnificent Years</div>
  </header>

  <div class="tabs">
    <div class="tab active" data-tab="cam">📷 &nbsp;Camera</div>
    <div class="tab" data-tab="up">🖼 &nbsp;Upload</div>
    <div class="tab" data-tab="gal">✨ &nbsp;Gallery</div>
  </div>

  <div class="panels">

    <!-- ── CAMERA PANEL ── -->
    <div class="panel active" id="panelCam">
      <div class="cvs-wrap" id="camWrap">
        <div class="cvs-placeholder" id="camPH">Starting camera…</div>
        <canvas id="liveC" style="display:none;"></canvas>
        <canvas id="snapC" style="display:none;"></canvas>
      </div>
      <div class="status" id="camSt">Requesting rear camera…</div>
      <div class="btnrow">
        <button class="btn outline" id="flipBtn"   onclick="flipCam()">🔁 Flip</button>
        <button class="btn gold"   id="snapBtn"   onclick="doSnap()">📸 Capture</button>
        <button class="btn outline" id="retakeBtn" onclick="doRetake()" hidden>🔄 Retake</button>
      </div>
      <div class="btnrow" id="camAfter" hidden>
        <button class="btn gold"    onclick="downloadCanvas(snapC,'elease_80th_birthday.png')">⬇ Download PNG</button>
        <button class="btn outline" onclick="addGallery(snapC)">➕ Gallery</button>
      </div>
    </div>

    <!-- ── UPLOAD PANEL ── -->
    <div class="panel" id="panelUp">
      <div class="drop" id="dropZ" onclick="document.getElementById('fi').click()">
        <p>✦ &nbsp; Tap to choose a photo &nbsp; ✦</p>
        <small>JPG · PNG · HEIC · any image</small>
      </div>
      <input type="file" id="fi" accept="image/*" style="display:none">
      <div class="cvs-wrap" id="upWrap" style="display:none;">
        <canvas id="upC"></canvas>
      </div>
      <div class="status" id="upSt"></div>
      <div class="btnrow" id="upAfter" hidden>
        <button class="btn gold"    onclick="downloadCanvas(upC,'elease_80th_birthday.png')">⬇ Download PNG</button>
        <button class="btn outline" onclick="addGallery(upC)">➕ Gallery</button>
      </div>
    </div>

  </div><!-- /panels -->

  <footer>🌿 &nbsp; Eighty years of love, grace, wisdom &amp; joy &nbsp; 🌿</footer>

</div><!-- /shell -->

<!-- Gallery overlay (outside shell so it can go full-screen) -->
<div id="galOverlay">
  <div class="gal-head">
    <span class="gal-title">✦ &nbsp; Captured Memories</span>
    <button class="btn outline" style="flex:0;padding:8px 14px;font-size:.65rem;" onclick="closeGal()">✕ Close</button>
  </div>
  <div class="btnrow" style="margin-bottom:10px;">
    <button class="btn danger" style="font-size:.62rem;padding:9px;" onclick="clearGal()">🗑 Clear All</button>
  </div>
  <div class="gal-grid" id="galGrid"></div>
  <div class="gal-empty" id="galEmpty">No photos yet — capture or upload to start your gallery!</div>
</div>

<video id="vid" autoplay playsinline muted style="position:fixed;opacity:0;pointer-events:none;width:1px;height:1px;"></video>

<script>
// ── SPARKLES ──────────────────────────────────────────────────
;(function(){{
  const bg=document.getElementById('sp');
  for(let i=0;i<90;i++){{
    const d=document.createElement('div');
    const sz=Math.random()*2.6+.7;
    d.style.cssText=`position:absolute;border-radius:50%;background:#ffe8a0;`
      +`width:${{sz}}px;height:${{sz}}px;`
      +`left:${{Math.random()*100}}%;top:${{Math.random()*100}}%;`
      +`opacity:0;animation:tw ${{2.4+Math.random()*4.5}}s ease-in-out ${{-Math.random()*7}}s infinite;`;
    bg.appendChild(d);
  }}
}})();

// ── FRAME ─────────────────────────────────────────────────────
const FRAME_SRC = 'data:image/png;base64,{FRAME_B64}';
const CUT = {{top:{CUT['top']},bottom:{CUT['bottom']},left:{CUT['left']},right:{CUT['right']}}};
const CUT_W = CUT.right - CUT.left;
const CUT_H = CUT.bottom - CUT.top;
const CUT_R = CUT_W / CUT_H;

const frameImg = new Image();
frameImg.src = FRAME_SRC;

function getFW(){{ return frameImg.naturalWidth  || 1054; }}
function getFH(){{ return frameImg.naturalHeight || 1067; }}

// Centre-crop source to CUT_R aspect ratio
function cropArgs(vw,vh){{
  let sx,sy,sw,sh;
  if(vw/vh > CUT_R){{ sh=vh; sw=Math.round(vh*CUT_R); sx=Math.round((vw-sw)/2); sy=0; }}
  else              {{ sw=vw; sh=Math.round(vw/CUT_R); sx=0; sy=Math.round((vh-sh)/2); }}
  return {{sx,sy,sw,sh}};
}}

// Composite photo+frame onto a given canvas
function composite(srcEl, dstCanvas){{
  const FW=getFW(), FH=getFH();
  dstCanvas.width=FW; dstCanvas.height=FH;
  const ctx=dstCanvas.getContext('2d');
  let vw,vh;
  if(srcEl.tagName==='VIDEO'){{ vw=srcEl.videoWidth; vh=srcEl.videoHeight; }}
  else{{ vw=srcEl.naturalWidth||srcEl.width; vh=srcEl.naturalHeight||srcEl.height; }}
  const {{sx,sy,sw,sh}}=cropArgs(vw,vh);
  ctx.drawImage(srcEl,sx,sy,sw,sh,CUT.left,CUT.top,CUT_W,CUT_H);
  ctx.drawImage(frameImg,0,0,FW,FH);
}}

// ── DOWNLOAD (proper Blob — works everywhere) ─────────────────
function downloadCanvas(canvas, filename){{
  canvas.toBlob(blob=>{{
    const url=URL.createObjectURL(blob);
    const a=document.createElement('a');
    a.href=url; a.download=filename;
    document.body.appendChild(a); a.click();
    setTimeout(()=>{{ document.body.removeChild(a); URL.revokeObjectURL(url); }},300);
  }},'image/png');
}}

// ── TABS ──────────────────────────────────────────────────────
document.querySelectorAll('.tab').forEach(t=>{{
  t.addEventListener('click',()=>{{
    const id=t.dataset.tab;
    if(id==='gal'){{ openGal(); return; }}
    document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(x=>x.classList.remove('active'));
    t.classList.add('active');
    document.getElementById('panel'+(id==='cam'?'Cam':'Up')).classList.add('active');
    if(id==='cam' && !stream) startCamera('environment');
  }});
}});

// ── CAMERA ────────────────────────────────────────────────────
const vid      = document.getElementById('vid');
const liveC    = document.getElementById('liveC');
const snapC    = document.getElementById('snapC');
const liveCtx  = liveC.getContext('2d');
const camSt    = document.getElementById('camSt');
const camPH    = document.getElementById('camPH');

let stream=null, facing='environment', animId=null, snapped=false;

async function startCamera(f){{
  if(stream) stream.getTracks().forEach(t=>t.stop());
  camSt.textContent='Starting '+(f==='environment'?'rear':'front')+' camera…';
  try{{
    stream=await navigator.mediaDevices.getUserMedia({{
      video:{{facingMode:{{ideal:f}},width:{{ideal:1920}},height:{{ideal:1080}}}},audio:false
    }});
    vid.srcObject=stream;
    await new Promise(r=>vid.onloadedmetadata=r);
    await vid.play();
    const s=stream.getVideoTracks()[0].getSettings();
    facing=s.facingMode||f;
    camSt.textContent=facing==='environment'?'📷 Rear camera — aim & capture':'🤳 Front camera active';
    camPH.style.display='none';
    liveC.style.display='block';
    if(!snapped) startLive();
  }}catch(e){{
    camSt.textContent='⚠ '+e.message;
  }}
}}

function startLive(){{
  if(animId) cancelAnimationFrame(animId);
  function draw(){{
    if(snapped) return;
    animId=requestAnimationFrame(draw);
    if(!vid.videoWidth||!vid.videoHeight||!frameImg.complete) return;
    const FW=getFW(),FH=getFH();
    if(liveC.width!==FW){{ liveC.width=FW; liveC.height=FH; }}
    composite(vid,liveC);
  }}
  draw();
}}

function doSnap(){{
  if(!vid.videoWidth) return;
  snapped=true;
  if(animId) cancelAnimationFrame(animId);
  composite(vid,snapC);
  liveC.style.display='none';
  snapC.style.display='block';
  document.getElementById('snapBtn').hidden=true;
  document.getElementById('flipBtn').hidden=true;
  document.getElementById('retakeBtn').hidden=false;
  document.getElementById('camAfter').hidden=false;
  camSt.textContent='✅ Photo captured!';
}}

function doRetake(){{
  snapped=false;
  liveC.style.display='block';
  snapC.style.display='none';
  document.getElementById('snapBtn').hidden=false;
  document.getElementById('flipBtn').hidden=false;
  document.getElementById('retakeBtn').hidden=true;
  document.getElementById('camAfter').hidden=true;
  camSt.textContent='📷 Ready — aim and capture';
  startLive();
}}

function flipCam(){{
  facing=facing==='environment'?'user':'environment';
  startCamera(facing);
}}

// ── UPLOAD ────────────────────────────────────────────────────
const upC   = document.getElementById('upC');
const upWrap= document.getElementById('upWrap');
const upSt  = document.getElementById('upSt');
const upAft = document.getElementById('upAfter');

document.getElementById('fi').addEventListener('change',e=>{{
  const file=e.target.files[0]; if(!file) return;
  upSt.textContent='Processing…';
  const reader=new FileReader();
  reader.onload=ev=>{{
    const img=new Image();
    img.onload=()=>{{
      function go(){{
        composite(img,upC);
        upWrap.style.display='';
        upAft.hidden=false;
        upSt.textContent='✅ Photo framed — download or save to gallery!';
      }}
      if(frameImg.complete&&frameImg.naturalWidth) go();
      else frameImg.onload=go;
    }};
    img.src=ev.target.result;
  }};
  reader.readAsDataURL(file);
}});

// ── GALLERY ───────────────────────────────────────────────────
const gallery=[];

function addGallery(canvas){{
  canvas.toBlob(blob=>{{
    const url=URL.createObjectURL(blob);
    gallery.unshift(url);
    renderGal();
    // quick feedback
    const btn=event.target;
    const orig=btn.textContent;
    btn.textContent='✅ Saved!';
    setTimeout(()=>btn.textContent=orig,1600);
  }},'image/png');
}}

function renderGal(){{
  const grid=document.getElementById('galGrid');
  const empty=document.getElementById('galEmpty');
  grid.innerHTML='';
  empty.style.display=gallery.length?'none':'block';
  gallery.forEach((url,i)=>{{
    const wrap=document.createElement('div'); wrap.className='gal-item';
    const img=document.createElement('img'); img.src=url;
    const btn=document.createElement('button'); btn.className='gal-dl'; btn.textContent='⬇ Save';
    btn.onclick=()=>{{
      const a=document.createElement('a');
      a.href=url; a.download=`elease_80th_${{i+1}}.png`;
      document.body.appendChild(a); a.click(); document.body.removeChild(a);
    }};
    wrap.appendChild(img); wrap.appendChild(btn); grid.appendChild(wrap);
  }});
}}

function openGal(){{ renderGal(); document.getElementById('galOverlay').classList.add('open'); }}
function closeGal(){{ document.getElementById('galOverlay').classList.remove('open'); }}
function clearGal(){{ gallery.length=0; renderGal(); }}

// ── BOOT ──────────────────────────────────────────────────────
function boot(){{ startCamera('environment'); }}
if(frameImg.complete&&frameImg.naturalWidth) boot();
else frameImg.onload=boot;

// Sync iframe height to Streamlit
function syncH(){{
  try{{ window.parent.postMessage({{type:'streamlit:setFrameHeight',height:document.body.scrollHeight}},'*'); }}catch(e){{}}
}}
setInterval(syncH,800);
</script>
</body>
</html>"""

# ── Render ────────────────────────────────────────────────────
if not FRAME_OK:
    st.error(
        "⚠️ **frame.png not found.**  "
        "Place your birthday frame image as `frame.png` in the same folder as `app.py`, then refresh.",
        icon="🖼",
    )
else:
    st_html(APP_HTML, height=780, scrolling=False)
