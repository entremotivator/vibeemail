import streamlit as st
import io, os, base64, json, datetime, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

st.set_page_config(
    page_title="✦ BUVIE WEEKEND – Photo Booth",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
html,body,[data-testid="stAppViewContainer"],[data-testid="stAppViewContainer"]>.main,
[data-testid="stMainBlockContainer"],section[data-testid="stMain"]{
  background:#060610!important;overflow:hidden!important;
  height:100vh!important;max-height:100vh!important;
}
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"]{display:none!important;}
#MainMenu,footer,header{visibility:hidden!important;}
.block-container{padding:0!important;max-width:100%!important;height:100vh!important;overflow:hidden!important;}
</style>
""", unsafe_allow_html=True)

# ── Frame ──────────────────────────────────────────────────────
FRAME_PATH = os.path.join(os.path.dirname(__file__), "buvie_frame_transparent.png")
try:
    with open(FRAME_PATH, "rb") as f:
        FRAME_B64 = base64.b64encode(f.read()).decode()
    FRAME_OK = True
except FileNotFoundError:
    FRAME_B64 = ""; FRAME_OK = False

CUT = dict(top=304, bottom=1223, left=176, right=911)

# ── Google Drive helpers ───────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_drive_service():
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        info = dict(st.secrets["gcp_service_account"])
        creds = service_account.Credentials.from_service_account_info(
            info, scopes=["https://www.googleapis.com/auth/drive"])
        return build("drive", "v3", credentials=creds)
    except:
        return None

@st.cache_data(show_spinner=False, ttl=86400)
def get_or_create_folder():
    svc = get_drive_service()
    if not svc: return None, None
    try:
        name = f"Buvie Weekend Photo Booth – {datetime.date.today().strftime('%b %d %Y')}"
        q = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        res = svc.files().list(q=q, fields="files(id)").execute().get("files", [])
        if res:
            fid = res[0]["id"]
        else:
            meta = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
            fid = svc.files().create(body=meta, fields="id").execute()["id"]
            svc.permissions().create(fileId=fid, body={"type":"anyone","role":"reader"}).execute()
            host = st.secrets.get("app", {}).get("host_email", "")
            if host:
                svc.permissions().create(
                    fileId=fid,
                    body={"type":"user","role":"writer","emailAddress":host},
                    sendNotificationEmail=False
                ).execute()
        return fid, f"https://drive.google.com/drive/folders/{fid}"
    except:
        return None, None

def upload_to_drive(img_bytes, filename, folder_id):
    try:
        from googleapiclient.http import MediaIoBaseUpload
        svc = get_drive_service()
        if not svc or not folder_id: return None, None, None, None
        meta = {"name": filename, "parents": [folder_id]}
        media = MediaIoBaseUpload(io.BytesIO(img_bytes), mimetype="image/png", resumable=False)
        fid = svc.files().create(body=meta, media_body=media, fields="id").execute()["id"]
        svc.permissions().create(fileId=fid, body={"type":"anyone","role":"reader"}).execute()
        return (fid,
                f"https://drive.google.com/file/d/{fid}/view",
                f"https://drive.google.com/thumbnail?id={fid}&sz=w600",
                f"https://drive.google.com/uc?export=download&id={fid}")
    except:
        return None, None, None, None

def list_drive_photos(folder_id):
    try:
        svc = get_drive_service()
        if not svc or not folder_id: return []
        q = f"'{folder_id}' in parents and mimeType='image/png' and trashed=false"
        files = svc.files().list(q=q, fields="files(id,name)",
                                 orderBy="createdTime desc", pageSize=50).execute().get("files",[])
        return [{"name":f["name"],
                 "thumb":f"https://drive.google.com/thumbnail?id={f['id']}&sz=w600",
                 "view": f"https://drive.google.com/file/d/{f['id']}/view",
                 "dl":   f"https://drive.google.com/uc?export=download&id={f['id']}"}
                for f in files]
    except:
        return []

# ── Session state ──────────────────────────────────────────────
if "folder_id" not in st.session_state:
    fid, furl = get_or_create_folder()
    st.session_state.folder_id  = fid  or ""
    st.session_state.folder_url = furl or ""
if "gallery" not in st.session_state:
    st.session_state.gallery = list_drive_photos(st.session_state.folder_id)

# Handle upload from query params
qp = st.query_params
if "img_b64" in qp and "img_name" in qp:
    try:
        img_bytes = base64.b64decode(qp["img_b64"])
        fname = qp["img_name"]
        fid2, view, thumb, dl = upload_to_drive(img_bytes, fname, st.session_state.folder_id)
        if fid2:
            st.session_state.gallery.insert(0, {"name":fname,"thumb":thumb,"view":view,"dl":dl})
    except:
        pass
    st.query_params.clear()
    st.rerun()

FOLDER_URL   = st.session_state.folder_url
DRIVE_OK     = "true" if st.session_state.folder_id else "false"
GALLERY_JSON = json.dumps(st.session_state.gallery)
SHARE_EMAIL  = st.secrets.get("app", {}).get("share_email",
               st.secrets.get("app", {}).get("host_email", ""))

# ── Build HTML ─────────────────────────────────────────────────
APP_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<style>
:root{{
  --gold:#d4af37;--gold2:#f0d870;--gold3:#fff8e0;
  --bg:#060610;--bg2:#0d0d22;--bg3:#141428;--bg4:#1a1a38;
  --border:rgba(212,175,55,.18);--safe:env(safe-area-inset-bottom,0px);
}}
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}}
html,body{{width:100%;height:100dvh;overflow:hidden;background:var(--bg);color:var(--gold);
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;}}
#sp{{position:fixed;inset:0;pointer-events:none;z-index:0;}}
@keyframes tw{{0%,100%{{opacity:0;transform:scale(.2)}}50%{{opacity:.3;transform:scale(1.5)}}}}
.shell{{position:relative;z-index:1;width:100%;height:100dvh;display:flex;flex-direction:column;overflow:hidden;}}
header{{text-align:center;padding:8px 16px 6px;background:rgba(6,6,16,.97);border-bottom:1px solid var(--border);flex-shrink:0;}}
header h1{{font-size:clamp(1rem,4vw,1.5rem);font-weight:900;letter-spacing:.16em;color:var(--gold3);text-shadow:0 0 28px rgba(255,245,200,.25);line-height:1.1;font-family:'Georgia',serif;}}
header .sub{{font-size:clamp(.65rem,2vw,.8rem);color:rgba(212,175,55,.45);letter-spacing:.1em;margin-top:2px;font-style:italic;}}
.drive-pill{{display:inline-flex;align-items:center;gap:5px;margin-top:4px;padding:3px 10px;border-radius:100px;border:1px solid rgba(212,175,55,.25);font-size:.6rem;letter-spacing:.1em;color:rgba(212,175,55,.5);font-style:italic;text-decoration:none;transition:all .2s;cursor:pointer;background:rgba(212,175,55,.04);}}
.drive-pill:hover{{border-color:var(--gold);color:var(--gold2);}}
.drive-dot{{width:6px;height:6px;border-radius:50%;background:#4ade80;box-shadow:0 0 5px rgba(74,222,128,.5);animation:pulse 2s infinite;}}
.drive-dot.off{{background:#555;box-shadow:none;animation:none;}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.3}}}}
.tabs{{display:flex;background:var(--bg2);border-bottom:1px solid var(--border);flex-shrink:0;}}
.tab{{flex:1;padding:9px 4px;text-align:center;font-size:.62rem;letter-spacing:.13em;text-transform:uppercase;color:rgba(212,175,55,.35);cursor:pointer;border-bottom:2px solid transparent;transition:all .2s;font-weight:700;position:relative;}}
.tab.active{{color:var(--gold2);border-bottom-color:var(--gold);background:rgba(212,175,55,.06);}}
.badge{{position:absolute;top:4px;right:12%;background:var(--gold);color:#060610;font-size:.48rem;font-weight:900;min-width:14px;height:14px;border-radius:7px;display:none;align-items:center;justify-content:center;padding:0 3px;}}
.badge.show{{display:flex;}}
.panels{{flex:1;position:relative;overflow:hidden;min-height:0;}}
.panel{{position:absolute;inset:0;display:flex;flex-direction:column;gap:5px;padding:6px;opacity:0;pointer-events:none;transition:opacity .18s;overflow:hidden;}}
.panel.active{{opacity:1;pointer-events:all;}}
.cvs-wrap{{flex:1;min-height:0;position:relative;border-radius:8px;overflow:hidden;border:1px solid var(--border);background:var(--bg3);display:flex;align-items:center;justify-content:center;}}
.cvs-wrap canvas{{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;}}
.ph{{color:rgba(212,175,55,.35);font-size:.85rem;text-align:center;padding:20px;line-height:1.8;font-style:italic;}}
.ph span{{font-size:2rem;display:block;margin-bottom:8px;opacity:.4;}}
.stbar{{display:flex;align-items:center;gap:7px;padding:5px 10px;background:var(--bg4);border:1px solid var(--border);border-radius:7px;font-size:.62rem;letter-spacing:.1em;color:rgba(212,175,55,.5);font-style:italic;flex-shrink:0;}}
.dot{{width:7px;height:7px;border-radius:50%;background:rgba(212,175,55,.25);flex-shrink:0;}}
.dot.live{{background:#4ade80;box-shadow:0 0 6px rgba(74,222,128,.6);animation:pulse 2s infinite;}}
.dot.warn{{background:#f97316;}}
.btnrow{{display:flex;gap:6px;flex-shrink:0;}}
.btn{{flex:1;padding:12px 6px;border:none;border-radius:7px;cursor:pointer;font-weight:700;font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;transition:all .15s;-webkit-appearance:none;}}
.btn:active{{opacity:.72;transform:scale(.97);}}
.btn[hidden]{{display:none!important;}}
.btn.gold{{background:linear-gradient(135deg,#5a4010,#c9a62e,#7a5c18,#e0bc4a,#6a4c10);color:#060610;box-shadow:0 4px 16px rgba(212,175,55,.35);flex:2;font-size:.75rem;}}
.btn.outline{{background:rgba(212,175,55,.07);border:1px solid rgba(212,175,55,.35);color:rgba(212,175,55,.75);}}
.btn.green{{background:rgba(74,222,128,.1);border:1px solid rgba(74,222,128,.35);color:#4ade80;}}
.btn.blue{{background:rgba(56,189,248,.1);border:1px solid rgba(56,189,248,.35);color:#38bdf8;}}
.btn.danger{{background:rgba(220,60,60,.08);border:1px solid rgba(200,70,70,.25);color:rgba(220,100,100,.85);}}
.drop{{border:2px dashed rgba(212,175,55,.25);border-radius:8px;padding:18px 12px;text-align:center;cursor:pointer;background:var(--bg2);transition:all .2s;flex-shrink:0;}}
.drop:hover,.drop.drag{{border-color:var(--gold);background:rgba(212,175,55,.04);}}
.drop .di{{font-size:2rem;margin-bottom:6px;opacity:.5;}}
.drop p{{font-size:.8rem;letter-spacing:.1em;color:rgba(212,175,55,.45);margin-bottom:3px;font-style:italic;}}
.drop small{{font-size:.6rem;color:rgba(212,175,55,.28);letter-spacing:.07em;}}
#uploadOverlay{{position:absolute;inset:0;background:rgba(6,6,16,.88);display:none;flex-direction:column;align-items:center;justify-content:center;gap:12px;z-index:50;border-radius:8px;}}
#uploadOverlay.show{{display:flex;}}
.spinner{{width:36px;height:36px;border:3px solid rgba(212,175,55,.15);border-top-color:var(--gold);border-radius:50%;animation:spin .8s linear infinite;}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.spin-txt{{font-size:.78rem;color:rgba(212,175,55,.65);font-style:italic;}}
#panelGal{{overflow-y:auto;-webkit-overflow-scrolling:touch;}}
.gal-header{{display:flex;align-items:center;justify-content:space-between;flex-shrink:0;}}
.gal-title-txt{{font-size:.75rem;letter-spacing:.18em;text-transform:uppercase;color:var(--gold2);font-weight:700;}}
.gal-count{{font-size:.7rem;color:rgba(212,175,55,.45);font-style:italic;}}
.gal-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:7px;}}
.gal-item{{position:relative;border-radius:7px;overflow:hidden;border:1px solid var(--border);background:var(--bg3);cursor:pointer;}}
.gal-item img{{width:100%;display:block;aspect-ratio:.78;object-fit:cover;}}
.gal-item-acts{{position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(6,6,16,.93));padding:20px 5px 5px;display:flex;gap:4px;opacity:0;transition:opacity .2s;}}
.gal-item:hover .gal-item-acts,.gal-item:active .gal-item-acts{{opacity:1;}}
.gab{{flex:1;padding:6px 3px;background:rgba(212,175,55,.15);border:1px solid rgba(212,175,55,.3);border-radius:5px;color:var(--gold2);cursor:pointer;font-weight:700;font-size:.52rem;letter-spacing:.07em;text-transform:uppercase;}}
.gal-empty{{text-align:center;color:rgba(212,175,55,.3);font-style:italic;font-size:.88rem;margin:40px auto;line-height:1.9;}}
.gal-empty span{{font-size:2.5rem;display:block;margin-bottom:10px;opacity:.35;}}
#sheet{{position:fixed;inset:0;z-index:500;display:none;flex-direction:column;justify-content:flex-end;}}
#sheet.open{{display:flex;}}
#sheetBg{{position:absolute;inset:0;background:rgba(4,4,14,.78);backdrop-filter:blur(4px);}}
#sheetBody{{position:relative;background:var(--bg2);border-radius:16px 16px 0 0;border:1px solid var(--border);padding:16px 14px calc(16px + var(--safe));display:flex;flex-direction:column;gap:9px;}}
.sh-title{{text-align:center;font-size:.7rem;letter-spacing:.18em;text-transform:uppercase;color:var(--gold2);padding-bottom:9px;border-bottom:1px solid rgba(212,175,55,.1);}}
.sh-btn{{width:100%;padding:13px;border:none;border-radius:9px;cursor:pointer;font-weight:700;font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;transition:all .15s;-webkit-appearance:none;}}
.sh-btn:active{{transform:scale(.97);opacity:.8;}}
.sh-btn.primary{{background:linear-gradient(135deg,#5a4010,#c9a62e,#7a5c18,#e0bc4a);color:#060610;}}
.sh-btn.drive{{background:rgba(74,222,128,.1);border:1px solid rgba(74,222,128,.3);color:#4ade80;}}
.sh-btn.email{{background:rgba(56,189,248,.1);border:1px solid rgba(56,189,248,.3);color:#38bdf8;}}
.sh-btn.gal{{background:rgba(212,175,55,.08);border:1px solid rgba(212,175,55,.28);color:rgba(212,175,55,.75);}}
.sh-btn.cancel{{background:transparent;border:1px solid rgba(212,175,55,.14);color:rgba(212,175,55,.38);}}
#toast{{position:fixed;bottom:calc(20px + var(--safe));left:50%;transform:translateX(-50%) translateY(16px);background:rgba(16,16,42,.97);border:1px solid var(--gold);color:var(--gold2);padding:9px 20px;border-radius:100px;font-size:.66rem;letter-spacing:.12em;font-weight:700;text-transform:uppercase;opacity:0;transition:all .28s;z-index:999;white-space:nowrap;pointer-events:none;}}
#toast.show{{opacity:1;transform:translateX(-50%) translateY(0);}}
footer{{text-align:center;padding:4px 16px calc(4px + var(--safe));font-size:.6rem;color:rgba(212,175,55,.18);letter-spacing:.06em;font-style:italic;border-top:1px solid var(--border);background:rgba(6,6,16,.97);flex-shrink:0;}}
</style>
</head>
<body>
<div id="sp"></div>
<div id="toast"></div>
<div id="sheet">
  <div id="sheetBg" onclick="closeSheet()"></div>
  <div id="sheetBody">
    <div class="sh-title" id="sheetTitle">Share Photo</div>
    <button class="sh-btn primary" onclick="sheetDo('download')">⬇ &nbsp;Save to Device</button>
    <button class="sh-btn drive"   onclick="sheetDo('drive')" id="sheetDriveBtn">☁ &nbsp;Save to Google Drive</button>
    <button class="sh-btn email"   onclick="sheetDo('email')">✉ &nbsp;Email This Photo</button>
    <button class="sh-btn gal"     onclick="sheetDo('gallery')">✨ &nbsp;Add to Gallery</button>
    <button class="sh-btn cancel"  onclick="closeSheet()">Cancel</button>
  </div>
</div>
<div class="shell">
  <header>
    <h1>✦ BUVIE WEEKEND ✦</h1>
    <div class="sub">Miami Birthday Celebration · Photo Booth</div>
    {'<a class="drive-pill" href="'+FOLDER_URL+'" target="_blank"><span class="drive-dot"></span>Drive folder ready</a>' if FOLDER_URL else '<div class="drive-pill"><span class="drive-dot off"></span>Drive not connected</div>'}
  </header>
  <div class="tabs">
    <div class="tab active" data-tab="cam">📷 Camera</div>
    <div class="tab"        data-tab="up">🖼 Upload</div>
    <div class="tab"        data-tab="gal">✨ Gallery <span class="badge" id="galBadge">0</span></div>
  </div>
  <div class="panels">
    <div class="panel active" id="panelCam">
      <div class="cvs-wrap">
        <div id="uploadOverlay"><div class="spinner"></div><div class="spin-txt" id="uploadTxt">Saving to Drive…</div></div>
        <div class="ph" id="camPH"><span>📷</span>Tap Start Camera below</div>
        <canvas id="liveC" style="display:none"></canvas>
        <canvas id="snapC" style="display:none"></canvas>
      </div>
      <div class="stbar"><span class="dot" id="camDot"></span><span id="camSt">Press Start Camera</span></div>
      <div class="btnrow" id="camControls">
        <button class="btn outline" onclick="flipCam()">🔁 Flip</button>
        <button class="btn green"   onclick="startCamera(facing)" id="startBtn">▶ Start Camera</button>
        <button class="btn gold"    onclick="doSnap()" id="snapBtn" hidden>📸 Capture</button>
      </div>
      <div class="btnrow" id="camAfter" hidden>
        <button class="btn outline" onclick="doRetake()">🔄 Retake</button>
        <button class="btn gold"    onclick="openSheet('cam')">Share ✦</button>
      </div>
    </div>
    <div class="panel" id="panelUp">
      <div class="drop" id="dropZ" onclick="document.getElementById('fi').click()"
           ondragover="this.classList.add('drag');event.preventDefault()"
           ondragleave="this.classList.remove('drag')"
           ondrop="handleDrop(event)">
        <div class="di">🖼</div>
        <p>✦ Tap to choose a photo ✦</p>
        <small>JPG · PNG · HEIC · any image</small>
      </div>
      <input type="file" id="fi" accept="image/*" style="display:none">
      <div class="cvs-wrap" id="upWrap" style="display:none"><canvas id="upC"></canvas></div>
      <div class="stbar" id="upStatus" style="display:none"><span class="dot live"></span><span id="upSt">Photo framed!</span></div>
      <div class="btnrow" id="upAfter" hidden>
        <button class="btn outline" onclick="clearUpload()">🔄 New</button>
        <button class="btn gold"    onclick="openSheet('up')">Share ✦</button>
      </div>
    </div>
    <div class="panel" id="panelGal">
      <div class="gal-header">
        <span class="gal-title-txt">✦ Captured Memories</span>
        <span class="gal-count" id="galCount">0 photos</span>
      </div>
      <div class="gal-grid" id="galGrid"></div>
      <div class="gal-empty" id="galEmpty"><span>📸</span>No photos yet!<br>Capture or upload to begin.</div>
    </div>
  </div>
  <footer>🎉 BUVIE WEEKEND – Miami Birthday Celebration 🎉</footer>
</div>
<video id="vid" autoplay playsinline muted
  style="position:fixed;opacity:0;pointer-events:none;width:1px;height:1px;top:0;left:0;"></video>
<script>
const DRIVE_OK={DRIVE_OK}, FOLDER_URL="{FOLDER_URL}", SHARE_EMAIL="{SHARE_EMAIL}";
let gallery={GALLERY_JSON};

// Sparkles
(function(){{const bg=document.getElementById('sp');for(let i=0;i<80;i++){{const d=document.createElement('div'),sz=Math.random()*2.5+.5;d.style.cssText=`position:absolute;width:${{sz}}px;height:${{sz}}px;background:#fff8e0;border-radius:${{Math.random()>.5?'50%':'2px'}};left:${{Math.random()*100}}%;top:${{Math.random()*100}}%;opacity:0;animation:tw ${{2.5+Math.random()*5}}s ease-in-out ${{-Math.random()*8}}s infinite;`;bg.appendChild(d);}}}})(  );

// Frame
const FRAME_SRC='data:image/png;base64,{FRAME_B64}';
const CUT={{top:{CUT['top']},bottom:{CUT['bottom']},left:{CUT['left']},right:{CUT['right']}}};
const CUT_W=CUT.right-CUT.left,CUT_H=CUT.bottom-CUT.top,CUT_R=CUT_W/CUT_H;
const frameImg=new Image(); frameImg.src=FRAME_SRC;
let frameReady=false; frameImg.onload=()=>{{frameReady=true; renderGal(); updateBadge();}};
function getFW(){{return frameImg.naturalWidth||1086;}}
function getFH(){{return frameImg.naturalHeight||1448;}}
function cropArgs(vw,vh){{
  let sx,sy,sw,sh;
  if(vw/vh>CUT_R){{sh=vh;sw=Math.round(vh*CUT_R);sx=Math.round((vw-sw)/2);sy=0;}}
  else{{sw=vw;sh=Math.round(vw/CUT_R);sx=0;sy=Math.round((vh-sh)/2);}}
  return{{sx,sy,sw,sh}};
}}
function composite(src,dst){{
  const FW=getFW(),FH=getFH();
  dst.width=FW;dst.height=FH;
  const ctx=dst.getContext('2d');
  let vw,vh;
  if(src.tagName==='VIDEO'){{vw=src.videoWidth;vh=src.videoHeight;}}
  else{{vw=src.naturalWidth||src.width;vh=src.naturalHeight||src.height;}}
  const{{sx,sy,sw,sh}}=cropArgs(vw,vh);
  ctx.drawImage(src,sx,sy,sw,sh,CUT.left,CUT.top,CUT_W,CUT_H);
  ctx.drawImage(frameImg,0,0,FW,FH);
}}

// Toast
let _tt;
function toast(msg,dur=2400){{const el=document.getElementById('toast');el.textContent=msg;el.classList.add('show');clearTimeout(_tt);_tt=setTimeout(()=>el.classList.remove('show'),dur);}}

// Tabs
document.querySelectorAll('.tab').forEach(t=>{{
  t.addEventListener('click',()=>{{
    const id=t.dataset.tab;
    document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(x=>x.classList.remove('active'));
    t.classList.add('active');
    document.getElementById({{cam:'panelCam',up:'panelUp',gal:'panelGal'}}[id]).classList.add('active');
    if(id==='gal') renderGal();
  }});
}});

// Camera
const vid=document.getElementById('vid');
const liveC=document.getElementById('liveC');
const snapC=document.getElementById('snapC');
let stream=null,facing='environment',animId=null,snapped=false;

function setStatus(msg,state){{
  document.getElementById('camSt').textContent=msg;
  const d=document.getElementById('camDot');
  d.className='dot'+(state==='live'?' live':state==='warn'?' warn':'');
}}

async function startCamera(f){{
  if(stream){{stream.getTracks().forEach(t=>t.stop());stream=null;}}
  setStatus('Starting camera…','');
  document.getElementById('startBtn').textContent='Starting…';
  document.getElementById('startBtn').disabled=true;

  if(!navigator.mediaDevices||!navigator.mediaDevices.getUserMedia){{
    setStatus('⚠ Camera blocked by browser — see note below','warn');
    document.getElementById('camPH').style.display='block';
    document.getElementById('camPH').innerHTML='<span>⚠</span><b>Camera blocked</b><br><small style="font-size:.72rem;opacity:.8">If using Streamlit Cloud, open this URL directly in your phone browser (not embedded). Camera requires HTTPS + direct page load.</small>';
    document.getElementById('startBtn').textContent='▶ Start Camera';
    document.getElementById('startBtn').disabled=false;
    return;
  }}

  const tries=[
    {{video:{{facingMode:{{ideal:f}},width:{{ideal:1280}},height:{{ideal:720}}}},audio:false}},
    {{video:{{facingMode:f}},audio:false}},
    {{video:true,audio:false}}
  ];
  let ok=false;
  for(const c of tries){{
    try{{stream=await navigator.mediaDevices.getUserMedia(c);ok=true;break;}}
    catch(e){{
      if(e.name==='NotAllowedError'||e.name==='PermissionDeniedError'){{
        setStatus('⚠ Camera permission denied — tap browser address bar → allow camera','warn');
        document.getElementById('startBtn').textContent='▶ Start Camera';
        document.getElementById('startBtn').disabled=false;
        return;
      }}
    }}
  }}
  if(!ok||!stream){{
    setStatus('⚠ Camera unavailable on this device','warn');
    document.getElementById('startBtn').textContent='▶ Start Camera';
    document.getElementById('startBtn').disabled=false;
    return;
  }}

  vid.srcObject=stream;
  await new Promise((res,rej)=>{{vid.onloadedmetadata=res;setTimeout(()=>rej(),8000);}}).catch(()=>{{}});
  try{{await vid.play();}}catch(e){{}}

  const s=stream.getVideoTracks()[0].getSettings();
  facing=s.facingMode||f;
  setStatus(facing==='environment'?'📷 Rear camera ready — tap Capture':'🤳 Front camera active','live');
  document.getElementById('camPH').style.display='none';
  liveC.style.display='block';
  document.getElementById('startBtn').hidden=true;
  document.getElementById('snapBtn').hidden=false;
  if(!snapped) startLive();
}}

function startLive(){{
  if(animId) cancelAnimationFrame(animId);
  function draw(){{
    if(snapped)return;
    animId=requestAnimationFrame(draw);
    if(!vid.videoWidth||!vid.videoHeight||!frameReady)return;
    const FW=getFW(),FH=getFH();
    if(liveC.width!==FW){{liveC.width=FW;liveC.height=FH;}}
    composite(vid,liveC);
  }}
  draw();
}}

function doSnap(){{
  if(!vid.videoWidth){{toast('⚠ Camera not ready'); return;}}
  snapped=true;
  if(animId) cancelAnimationFrame(animId);
  composite(vid,snapC);
  liveC.style.display='none'; snapC.style.display='block';
  document.getElementById('camControls').hidden=true;
  document.getElementById('camAfter').hidden=false;
  setStatus('✅ Captured! Tap Share to save.','live');
  toast('✦ Photo captured!');
}}

function doRetake(){{
  snapped=false;
  liveC.style.display='block'; snapC.style.display='none';
  document.getElementById('camControls').hidden=false;
  document.getElementById('camAfter').hidden=true;
  document.getElementById('startBtn').hidden=true;
  document.getElementById('snapBtn').hidden=false;
  setStatus('📷 Ready — aim and capture','live');
  startLive();
}}

function flipCam(){{
  facing=facing==='environment'?'user':'environment';
  if(stream) startCamera(facing);
}}

// Upload
const upC=document.getElementById('upC');
function handleDrop(e){{e.preventDefault();document.getElementById('dropZ').classList.remove('drag');const f=e.dataTransfer.files[0];if(f&&f.type.startsWith('image/')) processFile(f);}}
document.getElementById('fi').addEventListener('change',e=>{{if(e.target.files[0]) processFile(e.target.files[0]);}});
function processFile(file){{
  toast('✦ Processing…');
  const reader=new FileReader();
  reader.onload=ev=>{{
    const img=new Image();
    img.onload=()=>{{
      function go(){{composite(img,upC);document.getElementById('dropZ').style.display='none';document.getElementById('upWrap').style.display='';document.getElementById('upStatus').style.display='flex';document.getElementById('upAfter').hidden=false;document.getElementById('upSt').textContent='✅ Framed — tap Share!';toast('✦ Frame applied!');}}
      if(frameReady) go(); else frameImg.onload=go;
    }};
    img.src=ev.target.result;
  }};
  reader.readAsDataURL(file);
}}
function clearUpload(){{document.getElementById('dropZ').style.display='';document.getElementById('upWrap').style.display='none';document.getElementById('upStatus').style.display='none';document.getElementById('upAfter').hidden=true;document.getElementById('fi').value='';}}

// Gallery
function updateBadge(){{const b=document.getElementById('galBadge'),c=document.getElementById('galCount');b.textContent=gallery.length;b.classList.toggle('show',gallery.length>0);c.textContent=gallery.length+(gallery.length===1?' photo':' photos');}}
function addToGallery(canvas,fname){{canvas.toBlob(blob=>{{const url=URL.createObjectURL(blob);gallery.unshift({{name:fname,thumb:url,view:url,dl:url,local:true}});updateBadge();renderGal();toast('✦ Added to gallery!');}}, 'image/png');}}
function renderGal(){{
  const grid=document.getElementById('galGrid'),empty=document.getElementById('galEmpty');
  grid.innerHTML='';empty.style.display=gallery.length?'none':'block';
  gallery.forEach((item,i)=>{{
    const wrap=document.createElement('div');wrap.className='gal-item';
    const img=document.createElement('img');img.src=item.thumb||item.view;img.loading='lazy';
    const acts=document.createElement('div');acts.className='gal-item-acts';
    const dlBtn=document.createElement('button');dlBtn.className='gab';dlBtn.textContent='⬇ Save';
    dlBtn.onclick=e=>{{e.stopPropagation();if(item.local){{const a=document.createElement('a');a.href=item.dl;a.download=item.name||'photo.png';document.body.appendChild(a);a.click();document.body.removeChild(a);}}else window.open(item.dl,'_blank');toast('✦ Saved!');}}; 
    if(!item.local&&item.view){{const vBtn=document.createElement('button');vBtn.className='gab';vBtn.textContent='☁ View';vBtn.onclick=e=>{{e.stopPropagation();window.open(item.view,'_blank');}};acts.appendChild(vBtn);}}
    acts.appendChild(dlBtn);wrap.appendChild(img);wrap.appendChild(acts);grid.appendChild(wrap);
  }});
  updateBadge();
}}

// Drive upload
function blobToB64(blob){{return new Promise((res,rej)=>{{const r=new FileReader();r.onload=()=>res(r.result);r.onerror=rej;r.readAsDataURL(blob);}});}}
async function uploadToDrive(canvas,fname){{
  if(!DRIVE_OK){{toast('⚠ Drive not connected');return false;}}
  document.getElementById('uploadOverlay').classList.add('show');
  document.getElementById('uploadTxt').textContent='Saving to Drive…';
  try{{
    const blob=await new Promise(res=>canvas.toBlob(res,'image/png'));
    const b64=(await blobToB64(blob)).split(',')[1];
    const url=new URL(window.location.href);
    url.searchParams.set('img_b64',b64);url.searchParams.set('img_name',fname);
    window.location.href=url.toString();
    return true;
  }}catch(e){{document.getElementById('uploadOverlay').classList.remove('show');toast('⚠ Upload failed');return false;}}
}}

// Email
function emailPhoto(canvas,fname){{
  downloadCanvas(canvas,fname);
  setTimeout(()=>{{
    const sub=encodeURIComponent('✦ Buvie Weekend Birthday Photo');
    const bdy=encodeURIComponent('Photo from Buvie Weekend! 🎉\n\n'+(FOLDER_URL?'All photos: '+FOLDER_URL+'\n\n':'')+'✦ BUVIE WEEKEND – Miami Birthday');
    window.open(`mailto:${{SHARE_EMAIL}}?subject=${{sub}}&body=${{bdy}}`,'_blank');
    toast('✦ Email client opened!');
  }},600);
}}

// Download
function downloadCanvas(canvas,fname){{canvas.toBlob(blob=>{{const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=fname;document.body.appendChild(a);a.click();setTimeout(()=>{{document.body.removeChild(a);URL.revokeObjectURL(url);}},300);toast('✦ Saved to device!');}}, 'image/png');}}

// Sheet
let sheetSrc=null;
function openSheet(src){{
  sheetSrc=src;
  const ts=new Date().toISOString().slice(0,19).replace(/[T:]/g,'-');
  document.getElementById('sheetTitle').textContent='Share · '+ts;
  document.getElementById('sheetDriveBtn').textContent=DRIVE_OK?'☁  Save to Google Drive':'☁  Drive not connected';
  document.getElementById('sheetDriveBtn').disabled=!DRIVE_OK;
  document.getElementById('sheet').classList.add('open');
}}
function closeSheet(){{document.getElementById('sheet').classList.remove('open');}}
function sheetDo(action){{
  closeSheet();
  const canvas=sheetSrc==='cam'?snapC:upC;
  const ts=new Date().toISOString().slice(0,10);
  const fname=`buvie_weekend_${{ts}}_${{Date.now()%10000}}.png`;
  if(action==='download') downloadCanvas(canvas,fname);
  else if(action==='drive') uploadToDrive(canvas,fname);
  else if(action==='email') emailPhoto(canvas,fname);
  else if(action==='gallery') addToGallery(canvas,fname);
}}

// Boot — no auto-start camera, user must tap button (bypasses iframe permission issues)
renderGal(); updateBadge();

// Try patching parent iframe permissions
try{{
  window.parent.document.querySelectorAll('iframe').forEach(f=>{{
    const a=f.getAttribute('allow')||'';
    if(!a.includes('camera')) f.setAttribute('allow',a?a+'; camera *; microphone *':'camera *; microphone *');
  }});
}}catch(e){{}}
</script>
</body>
</html>"""

# ── Render ─────────────────────────────────────────────────────
if not FRAME_OK:
    st.error("⚠️ **buvie_frame_transparent.png not found.** Place it in the same folder as app.py.", icon="🖼")
else:
    # Patch parent iframes to allow camera BEFORE the component renders
    st.components.v1.html("""<script>
    (function(){
      function patch(){
        try{
          var frames=window.parent.document.querySelectorAll('iframe');
          frames.forEach(function(f){
            var a=f.getAttribute('allow')||'';
            if(!a.includes('camera'))
              f.setAttribute('allow',a?a+'; camera *; microphone *':'camera *; microphone *');
          });
        }catch(e){}
      }
      patch();
      try{new window.parent.MutationObserver(patch).observe(window.parent.document.body,{childList:true,subtree:true});}catch(e){}
    })();
    </script>""", height=0)

    from streamlit.components.v1 import html as st_html
    st_html(APP_HTML, height=820, scrolling=False)
