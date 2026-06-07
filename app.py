import streamlit as st
import os, base64, io, json, time, datetime
from streamlit.components.v1 import html as st_html

st.set_page_config(
    page_title="✦ BUVIE WEEKEND – Birthday Celebration",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&display=swap');
html,body,[data-testid="stAppViewContainer"],[data-testid="stAppViewContainer"]>.main,
[data-testid="stMainBlockContainer"],section[data-testid="stMain"]{{
  background:#060612!important;overflow:hidden!important;
  height:100vh!important;max-height:100vh!important;
}}
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"]{{display:none!important;}}
#MainMenu,footer,header{{visibility:hidden!important;}}
.block-container{{padding:0!important;max-width:100%!important;height:100vh!important;overflow:hidden!important;}}
</style>
""", unsafe_allow_html=True)

# ── Google Drive helper ───────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_drive_service():
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        creds_dict = dict(st.secrets["gcp_service_account"])
        creds = service_account.Credentials.from_service_account_info(
            creds_dict,
            scopes=["https://www.googleapis.com/auth/drive"]
        )
        return build("drive", "v3", credentials=creds)
    except Exception as e:
        return None

@st.cache_data(show_spinner=False, ttl=3600)
def get_or_create_folder(event_name: str) -> dict:
    """Returns {folder_id, folder_url} — creates once per session."""
    svc = get_drive_service()
    if not svc:
        return {"folder_id": None, "folder_url": None, "error": "Drive not connected"}
    try:
        share_email = st.secrets.get("app", {}).get("share_email", "entremotivator@gmail.com")
        folder_name = f"{event_name} – Photo Booth {datetime.date.today().strftime('%b %d %Y')}"
        meta = {"name": folder_name, "mimeType": "application/vnd.google-apps.folder"}
        folder = svc.files().create(body=meta, fields="id").execute()
        fid = folder["id"]
        # Share with target email
        svc.permissions().create(
            fileId=fid,
            body={"type": "user", "role": "writer", "emailAddress": share_email},
            sendNotificationEmail=True,
        ).execute()
        # Make publicly viewable via link
        svc.permissions().create(
            fileId=fid,
            body={"type": "anyone", "role": "reader"},
        ).execute()
        url = f"https://drive.google.com/drive/folders/{fid}"
        return {"folder_id": fid, "folder_url": url, "folder_name": folder_name}
    except Exception as e:
        return {"folder_id": None, "folder_url": None, "error": str(e)}

def upload_to_drive(img_bytes: bytes, filename: str, folder_id: str) -> dict:
    """Upload PNG bytes to Drive folder, return {file_id, view_url, thumbnail_url}."""
    try:
        from googleapiclient.http import MediaIoBaseUpload
        svc = get_drive_service()
        if not svc or not folder_id:
            return {}
        meta = {"name": filename, "parents": [folder_id]}
        media = MediaIoBaseUpload(io.BytesIO(img_bytes), mimetype="image/png", resumable=False)
        f = svc.files().create(body=meta, media_body=media, fields="id").execute()
        fid = f["id"]
        svc.permissions().create(
            fileId=fid, body={"type": "anyone", "role": "reader"}
        ).execute()
        view_url  = f"https://drive.google.com/file/d/{fid}/view"
        dl_url    = f"https://drive.google.com/uc?export=download&id={fid}"
        thumb_url = f"https://drive.google.com/thumbnail?id={fid}&sz=w400"
        return {"file_id": fid, "view_url": view_url, "dl_url": dl_url, "thumb_url": thumb_url}
    except Exception as e:
        return {"error": str(e)}

# ── Load frame ───────────────────────────────────────────────
FRAME_PATH = os.path.join(os.path.dirname(__file__), "buvie_frame_transparent.png")
try:
    with open(FRAME_PATH, "rb") as f:
        FRAME_B64 = base64.b64encode(f.read()).decode()
    FRAME_OK = True
except FileNotFoundError:
    FRAME_B64 = ""
    FRAME_OK = False

CUT = dict(top=289, bottom=1231, left=162, right=924)

# ── Session state ────────────────────────────────────────────
if "drive_folder" not in st.session_state:
    event_name = st.secrets.get("app", {}).get("event_name", "Buvie Weekend Birthday")
    st.session_state.drive_folder = get_or_create_folder(event_name)
if "gallery" not in st.session_state:
    st.session_state.gallery = []  # list of {thumb_url, view_url, dl_url, filename}
if "upload_queue" not in st.session_state:
    st.session_state.upload_queue = []

# Handle incoming upload from JS via query param trick
qp = st.query_params
if "upload_b64" in qp and "upload_name" in qp:
    try:
        img_bytes = base64.b64decode(qp["upload_b64"])
        fname     = qp["upload_name"]
        folder    = st.session_state.drive_folder
        if folder.get("folder_id"):
            result = upload_to_drive(img_bytes, fname, folder["folder_id"])
            if "file_id" in result:
                st.session_state.gallery.append({
                    "thumb_url": result["thumb_url"],
                    "view_url":  result["view_url"],
                    "dl_url":    result["dl_url"],
                    "filename":  fname,
                })
    except:
        pass
    st.query_params.clear()
    st.rerun()

# ── Build gallery JSON for JS ────────────────────────────────
gallery_json = json.dumps(st.session_state.gallery)
folder_info  = st.session_state.drive_folder
folder_url   = folder_info.get("folder_url", "") or ""
folder_name  = folder_info.get("folder_name", "Buvie Weekend")
share_email  = st.secrets.get("app", {}).get("share_email", "entremotivator@gmail.com")
drive_ok     = bool(folder_info.get("folder_id"))

APP_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&display=swap" rel="stylesheet">
<style>
:root{{
  --gold:#d4af37;--gold2:#f0d87a;--gold3:#fff9e6;
  --bg:#060612;--bg2:#0d0d22;--bg3:#13132e;--bg4:#1a1a3a;
  --border:rgba(212,175,55,.18);--bordH:rgba(212,175,55,.4);
  --faint:rgba(212,175,55,.1);--safe:env(safe-area-inset-bottom,0px);
}}
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}}
html,body{{width:100%;height:100vh;overflow:hidden;background:var(--bg);font-family:'Playfair Display',serif;color:var(--gold);}}
#sp{{position:fixed;inset:0;pointer-events:none;z-index:0;overflow:hidden;}}
@keyframes tw{{0%,100%{{opacity:0;transform:scale(.3)}}50%{{opacity:.4;transform:scale(1.5)}}}}
.shell{{position:relative;z-index:1;width:100%;height:100vh;display:flex;flex-direction:column;overflow:hidden;}}

/* HEADER */
header{{text-align:center;padding:10px 16px 8px;border-bottom:1px solid var(--border);background:rgba(6,6,18,.98);flex-shrink:0;}}
header .crown{{font-size:1.4rem;margin-bottom:2px;}}
header h1{{font-size:clamp(1rem,4.5vw,1.5rem);font-weight:900;letter-spacing:.16em;color:var(--gold3);text-shadow:0 0 30px rgba(255,245,200,.2);line-height:1.1;}}
header .sub{{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:clamp(.7rem,2vw,.85rem);color:rgba(212,175,55,.45);letter-spacing:.1em;margin-top:3px;}}
.drive-pill{{display:inline-flex;align-items:center;gap:6px;margin-top:5px;padding:4px 12px;
  border:1px solid rgba(212,175,55,.25);border-radius:100px;
  font-size:.6rem;letter-spacing:.1em;color:rgba(212,175,55,.5);
  font-family:'Cormorant Garamond',serif;font-style:italic;cursor:pointer;
  background:rgba(212,175,55,.04);text-decoration:none;transition:all .2s;}}
.drive-pill:hover{{border-color:var(--gold);color:var(--gold2);}}
.drive-pill .dot{{width:6px;height:6px;border-radius:50%;background:#4ade80;box-shadow:0 0 5px rgba(74,222,128,.5);animation:pls 2s infinite;}}
.drive-pill .dot.off{{background:#666;box-shadow:none;animation:none;}}
@keyframes pls{{0%,100%{{opacity:1}}50%{{opacity:.3}}}}

/* TABS */
.tabs{{display:flex;border-bottom:1px solid var(--border);background:var(--bg2);flex-shrink:0;}}
.tab{{flex:1;padding:10px 4px;text-align:center;font-size:.65rem;letter-spacing:.13em;text-transform:uppercase;
  color:rgba(212,175,55,.35);cursor:pointer;border-bottom:2px solid transparent;transition:all .22s;
  font-family:'Playfair Display',serif;font-weight:700;position:relative;}}
.tab.active{{color:var(--gold2);border-bottom-color:var(--gold);background:rgba(212,175,55,.05);}}
.badge{{position:absolute;top:5px;right:14%;background:var(--gold);color:#060612;
  font-size:.5rem;font-weight:900;width:15px;height:15px;border-radius:50%;
  display:none;align-items:center;justify-content:center;}}
.badge.show{{display:flex;}}

/* PANELS */
.panels{{flex:1;position:relative;overflow:hidden;min-height:0;}}
.panel{{position:absolute;inset:0;display:flex;flex-direction:column;padding:10px 10px 8px;gap:8px;
  opacity:0;pointer-events:none;transition:opacity .2s;overflow:hidden;}}
.panel.active{{opacity:1;pointer-events:all;}}
#panelGal{{overflow-y:auto;-webkit-overflow-scrolling:touch;}}

/* CANVAS WRAP */
.cvs-wrap{{flex:1;min-height:0;position:relative;border-radius:10px;overflow:hidden;
  border:1px solid var(--border);background:var(--bg3);display:flex;align-items:center;justify-content:center;}}
.cvs-wrap canvas{{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;}}
.ph{{font-family:'Cormorant Garamond',serif;font-style:italic;color:rgba(212,175,55,.35);
  font-size:.88rem;letter-spacing:.08em;text-align:center;padding:20px;line-height:1.8;}}
.ph .i{{font-size:2rem;display:block;margin-bottom:8px;opacity:.5;}}

/* STATUS */
.st-bar{{display:flex;align-items:center;gap:8px;padding:6px 12px;background:var(--bg4);
  border:1px solid var(--border);border-radius:8px;font-size:.65rem;letter-spacing:.1em;
  color:rgba(212,175,55,.55);font-family:'Cormorant Garamond',serif;font-style:italic;flex-shrink:0;}}
.dot{{width:7px;height:7px;border-radius:50%;background:rgba(212,175,55,.3);flex-shrink:0;}}
.dot.live{{background:#4ade80;box-shadow:0 0 6px rgba(74,222,128,.6);animation:pls 2s infinite;}}
.dot.warn{{background:#f97316;box-shadow:0 0 6px rgba(249,115,22,.5);}}

/* BUTTONS */
.btnrow{{display:flex;gap:8px;flex-shrink:0;}}
.btn{{flex:1;padding:12px 6px;border:none;border-radius:8px;cursor:pointer;
  font-family:'Playfair Display',serif;font-weight:700;font-size:.68rem;letter-spacing:.1em;
  text-transform:uppercase;transition:all .15s;}}
.btn:active{{opacity:.75;transform:scale(.97);}}
.btn[hidden]{{display:none!important;}}
.btn.gold{{background:linear-gradient(135deg,#5a4010,#c9a62e,#7a5c18,#e0bc4a,#6a4c10);
  color:#060612;box-shadow:0 4px 18px rgba(212,175,55,.3);flex:2;font-size:.74rem;}}
.btn.outline{{background:rgba(212,175,55,.07);border:1px solid rgba(212,175,55,.32);color:rgba(212,175,55,.7);}}
.btn.outline:hover{{background:rgba(212,175,55,.12);border-color:rgba(212,175,55,.5);}}
.btn.green{{background:rgba(74,222,128,.1);border:1px solid rgba(74,222,128,.32);color:#4ade80;}}
.btn.blue{{background:rgba(56,189,248,.1);border:1px solid rgba(56,189,248,.32);color:#38bdf8;}}
.btn.purple{{background:rgba(168,85,247,.1);border:1px solid rgba(168,85,247,.32);color:#c084fc;}}
.btn.danger{{background:rgba(220,60,60,.08);border:1px solid rgba(200,70,70,.25);color:rgba(220,100,100,.85);}}

/* DROP ZONE */
.drop{{border:2px dashed rgba(212,175,55,.22);border-radius:10px;padding:20px 16px;text-align:center;
  cursor:pointer;background:var(--bg2);transition:all .2s;flex-shrink:0;}}
.drop:hover,.drop.drag{{border-color:var(--gold);background:rgba(212,175,55,.04);}}
.drop .di{{font-size:2rem;margin-bottom:8px;opacity:.6;}}
.drop p{{font-size:.82rem;letter-spacing:.1em;color:rgba(212,175,55,.5);margin-bottom:4px;
  font-family:'Cormorant Garamond',serif;font-style:italic;}}
.drop small{{font-size:.62rem;color:rgba(212,175,55,.28);letter-spacing:.07em;font-family:'Cormorant Garamond',serif;}}

/* GALLERY */
.gal-top{{display:flex;align-items:center;justify-content:space-between;flex-shrink:0;}}
.gal-title{{font-size:.75rem;letter-spacing:.18em;text-transform:uppercase;color:var(--gold2);}}
.gal-ct{{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:.72rem;color:rgba(212,175,55,.45);}}
.gal-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;overflow-y:auto;flex:1;min-height:0;}}
.gal-item{{position:relative;border-radius:8px;overflow:hidden;border:1px solid var(--border);
  background:var(--bg3);aspect-ratio:.62;cursor:pointer;}}
.gal-item img{{width:100%;height:100%;object-fit:cover;display:block;}}
.gal-actions{{position:absolute;bottom:0;left:0;right:0;
  background:linear-gradient(transparent,rgba(6,6,18,.92));
  padding:24px 6px 6px;display:flex;gap:5px;opacity:0;transition:opacity .2s;}}
.gal-item:hover .gal-actions,.gal-item:active .gal-actions{{opacity:1;}}
.gal-ab{{flex:1;padding:7px 3px;background:rgba(212,175,55,.15);border:1px solid rgba(212,175,55,.28);
  border-radius:6px;color:var(--gold2);cursor:pointer;font-family:'Playfair Display',serif;
  font-weight:700;font-size:.55rem;letter-spacing:.07em;text-transform:uppercase;}}
.gal-empty{{text-align:center;color:rgba(212,175,55,.3);font-family:'Cormorant Garamond',serif;
  font-style:italic;font-size:.9rem;margin:50px auto;line-height:1.8;}}
.gal-empty .ei{{font-size:2.5rem;display:block;margin-bottom:12px;opacity:.35;}}

/* ACTION SHEET */
#sheet{{position:fixed;inset:0;z-index:500;display:none;flex-direction:column;justify-content:flex-end;}}
#sheet.open{{display:flex;}}
#sheet-bg{{position:absolute;inset:0;background:rgba(4,4,16,.75);backdrop-filter:blur(4px);}}
#sheet-body{{position:relative;background:var(--bg2);border-radius:18px 18px 0 0;
  border:1px solid var(--border);padding:18px 16px calc(18px + var(--safe));
  display:flex;flex-direction:column;gap:10px;}}
.sheet-title{{text-align:center;font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;
  color:var(--gold2);padding-bottom:10px;border-bottom:1px solid var(--faint);}}
.sheet-btn{{width:100%;padding:14px;border:none;border-radius:10px;cursor:pointer;
  font-family:'Playfair Display',serif;font-weight:700;font-size:.75rem;letter-spacing:.12em;
  text-transform:uppercase;transition:all .15s;}}
.sheet-btn:active{{transform:scale(.97);opacity:.8;}}
.sheet-btn.primary{{background:linear-gradient(135deg,#5a4010,#c9a62e,#7a5c18,#e0bc4a);color:#060612;}}
.sheet-btn.sec{{background:rgba(212,175,55,.08);border:1px solid rgba(212,175,55,.28);color:rgba(212,175,55,.75);}}
.sheet-btn.eml{{background:rgba(56,189,248,.1);border:1px solid rgba(56,189,248,.3);color:#38bdf8;}}
.sheet-btn.drv{{background:rgba(74,222,128,.1);border:1px solid rgba(74,222,128,.3);color:#4ade80;}}
.sheet-btn.cancel{{background:transparent;border:1px solid rgba(212,175,55,.15);color:rgba(212,175,55,.4);}}

/* TOAST */
#toast{{position:fixed;bottom:calc(22px + var(--safe));left:50%;transform:translateX(-50%) translateY(20px);
  background:rgba(20,20,50,.97);border:1px solid var(--gold);color:var(--gold2);
  padding:10px 22px;border-radius:100px;font-size:.68rem;letter-spacing:.12em;
  font-family:'Playfair Display',serif;font-weight:700;text-transform:uppercase;
  opacity:0;transition:all .3s;z-index:999;white-space:nowrap;pointer-events:none;}}
#toast.show{{opacity:1;transform:translateX(-50%) translateY(0);}}

/* UPLOAD PROGRESS */
#uprogress{{position:absolute;inset:0;background:rgba(6,6,18,.85);display:none;
  flex-direction:column;align-items:center;justify-content:center;gap:12px;z-index:10;border-radius:10px;}}
#uprogress.show{{display:flex;}}
.spinner{{width:36px;height:36px;border:3px solid rgba(212,175,55,.15);
  border-top-color:var(--gold);border-radius:50%;animation:spin .8s linear infinite;}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.prog-txt{{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:.82rem;
  color:rgba(212,175,55,.7);letter-spacing:.08em;}}

footer{{text-align:center;padding:5px 16px calc(5px + var(--safe));font-family:'Cormorant Garamond',serif;
  font-style:italic;font-size:.65rem;color:rgba(212,175,55,.2);letter-spacing:.06em;
  border-top:1px solid var(--border);background:rgba(6,6,18,.98);flex-shrink:0;}}
::-webkit-scrollbar{{width:4px;}}
::-webkit-scrollbar-track{{background:transparent;}}
::-webkit-scrollbar-thumb{{background:rgba(212,175,55,.2);border-radius:2px;}}
</style>
</head>
<body>
<div id="sp"></div>
<div id="toast"></div>

<!-- ACTION SHEET -->
<div id="sheet">
  <div id="sheet-bg" onclick="closeSheet()"></div>
  <div id="sheet-body">
    <div class="sheet-title" id="sheet-title">Share Photo</div>
    <button class="sheet-btn primary" onclick="sheetAction('download')">⬇ &nbsp;Save to Device</button>
    <button class="sheet-btn drv"     onclick="sheetAction('drive')">☁ &nbsp;Save to Google Drive</button>
    <button class="sheet-btn eml"     onclick="sheetAction('email')">✉ &nbsp;Email This Photo</button>
    <button class="sheet-btn sec"     onclick="sheetAction('gallery')">➕ &nbsp;Add to Gallery</button>
    <button class="sheet-btn cancel"  onclick="closeSheet()">Cancel</button>
  </div>
</div>

<div class="shell">
  <header>
    <div class="crown">👑</div>
    <h1>BUVIE WEEKEND</h1>
    <div class="sub">Miami Birthday Celebration &nbsp;·&nbsp; Photo Booth</div>
    {f'<a class="drive-pill" href="{folder_url}" target="_blank"><span class="dot"></span>Drive folder ready · Open</a>' if drive_ok else '<div class="drive-pill"><span class="dot off"></span>Drive not connected</div>'}
  </header>

  <div class="tabs">
    <div class="tab active" data-tab="cam">📷 Camera</div>
    <div class="tab" data-tab="up">🖼 Upload</div>
    <div class="tab" data-tab="gal">✨ Gallery <span class="badge" id="galBadge">0</span></div>
  </div>

  <div class="panels">

    <!-- CAMERA -->
    <div class="panel active" id="panelCam">
      <div class="cvs-wrap" id="camWrap">
        <div id="uprogress"><div class="spinner"></div><div class="prog-txt" id="progTxt">Uploading to Drive…</div></div>
        <div class="ph" id="camPH"><span class="i">📷</span>Starting camera…<br><small style="font-size:.7rem;opacity:.65">Allow camera access to continue</small></div>
        <canvas id="liveC" style="display:none"></canvas>
        <canvas id="snapC" style="display:none"></canvas>
      </div>
      <div class="st-bar"><span class="dot" id="camDot"></span><span id="camSt">Requesting camera…</span></div>
      <div class="btnrow" id="camControls">
        <button class="btn outline" onclick="flipCam()">🔁 Flip</button>
        <button class="btn gold"    onclick="doSnap()">📸 Capture</button>
      </div>
      <div class="btnrow" id="camAfter" hidden>
        <button class="btn outline"  onclick="doRetake()">🔄 Retake</button>
        <button class="btn gold"     onclick="openSheet('cam')">Share ✦</button>
      </div>
    </div>

    <!-- UPLOAD -->
    <div class="panel" id="panelUp">
      <div class="drop" id="dropZ" onclick="document.getElementById('fi').click()"
           ondragover="this.classList.add('drag');event.preventDefault()"
           ondragleave="this.classList.remove('drag')"
           ondrop="handleDrop(event)">
        <div class="di">🖼</div>
        <p>✦ &nbsp;Tap to choose a photo&nbsp; ✦</p>
        <small>JPG · PNG · HEIC · any image format</small>
      </div>
      <input type="file" id="fi" accept="image/*" style="display:none">
      <div class="cvs-wrap" id="upWrap" style="display:none">
        <div id="uprogress2"><div class="spinner" id="sp2" style="display:none"></div><div class="prog-txt" id="progTxt2"></div></div>
        <canvas id="upC"></canvas>
      </div>
      <div class="st-bar" id="upStatus" style="display:none">
        <span class="dot live"></span><span id="upSt">Photo framed!</span>
      </div>
      <div class="btnrow" id="upAfter" hidden>
        <button class="btn outline"  onclick="clearUpload()">🔄 New</button>
        <button class="btn gold"     onclick="openSheet('up')">Share ✦</button>
      </div>
    </div>

    <!-- GALLERY -->
    <div class="panel" id="panelGal">
      <div class="gal-top">
        <span class="gal-title">✦ &nbsp;Captured Memories</span>
        <span class="gal-ct" id="galCt">0 photos</span>
      </div>
      {f'<a class="drive-pill" href="{folder_url}" target="_blank" style="margin-bottom:2px;"><span class="dot"></span>View full Drive folder</a>' if drive_ok else ''}
      <div class="gal-grid" id="galGrid"></div>
      <div class="gal-empty" id="galEmpty"><span class="ei">📸</span>No memories yet!<br>Capture or upload a photo<br>to start your gallery.</div>
      <div class="btnrow" style="flex-shrink:0;margin-top:4px;" id="galActions" hidden>
        <button class="btn danger"  onclick="clearGal()">🗑 Clear</button>
        <button class="btn blue"    onclick="openDrive()">☁ Drive</button>
        <button class="btn outline" onclick="downloadAll()">⬇ All</button>
      </div>
    </div>

  </div>

  <footer>🎉 &nbsp; BUVIE WEEKEND – Miami Birthday &nbsp; 🎉</footer>
</div>

<video id="vid" autoplay playsinline muted style="position:fixed;opacity:0;pointer-events:none;width:1px;height:1px;"></video>

<script>
// ── IFRAME CAMERA PERMISSION FIX ─────────────────────────────
// Streamlit renders st_html inside an iframe without allow="camera".
// We patch the iframe's allow attribute from inside using postMessage
// and also directly try to set it from within the frame.
(function patchCameraPermission() {{
  try {{
    // Try patching own iframe element from parent
    const iframes = window.parent.document.querySelectorAll('iframe');
    iframes.forEach(f => {{
      const cur = f.allow || '';
      if (!cur.includes('camera')) {{
        f.allow = cur ? cur + '; camera' : 'camera; microphone';
      }}
    }});
  }} catch(e) {{
    // Cross-origin parent — can't patch directly.
    // As a fallback, we rely on the Permissions API below.
  }}
}})();

// CONFIG
const DRIVE_OK     = {'true' if drive_ok else 'false'};
const FOLDER_URL   = "{folder_url}";
const SHARE_EMAIL  = "{share_email}";
const FOLDER_NAME  = "{folder_name}";

// ── SPARKLES ──────────────────────────────────────────────────
(function(){{
  const bg=document.getElementById('sp');
  for(let i=0;i<110;i++){{
    const d=document.createElement('div');
    const sz=Math.random()*2.8+.4;
    d.style.cssText=`position:absolute;width:${{sz}}px;height:${{sz}}px;`
      +`background:#fff9e0;border-radius:${{Math.random()>.5?'50%':'2px'}};`
      +`left:${{Math.random()*100}}%;top:${{Math.random()*100}}%;`
      +`opacity:0;animation:tw ${{2.5+Math.random()*5}}s ease-in-out ${{-Math.random()*8}}s infinite;`;
    bg.appendChild(d);
  }}
}})();

// ── FRAME ─────────────────────────────────────────────────────
const FRAME_SRC='{f"data:image/png;base64,{FRAME_B64}" if FRAME_OK else ""}';
const CUT={{top:{CUT['top']},bottom:{CUT['bottom']},left:{CUT['left']},right:{CUT['right']}}};
const CUT_W=CUT.right-CUT.left, CUT_H=CUT.bottom-CUT.top, CUT_R=CUT_W/CUT_H;
const frameImg=new Image(); frameImg.src=FRAME_SRC;
let frameReady=false; frameImg.onload=()=>{{frameReady=true;}};
function getFW(){{return frameImg.naturalWidth||861;}}
function getFH(){{return frameImg.naturalHeight||1618;}}
function cropArgs(vw,vh){{
  let sx,sy,sw,sh;
  if(vw/vh>CUT_R){{sh=vh;sw=Math.round(vh*CUT_R);sx=Math.round((vw-sw)/2);sy=0;}}
  else{{sw=vw;sh=Math.round(vw/CUT_R);sx=0;sy=Math.round((vh-sh)/2);}}
  return {{sx,sy,sw,sh}};
}}
function composite(src,dst){{
  const FW=getFW(),FH=getFH();
  dst.width=FW;dst.height=FH;
  const ctx=dst.getContext('2d');
  let vw,vh;
  if(src.tagName==='VIDEO'){{vw=src.videoWidth;vh=src.videoHeight;}}
  else{{vw=src.naturalWidth||src.width;vh=src.naturalHeight||src.height;}}
  const {{sx,sy,sw,sh}}=cropArgs(vw,vh);
  ctx.drawImage(src,sx,sy,sw,sh,CUT.left,CUT.top,CUT_W,CUT_H);
  ctx.drawImage(frameImg,0,0,FW,FH);
}}

// ── TOAST ─────────────────────────────────────────────────────
let _tt;
function toast(msg,dur=2400){{
  const el=document.getElementById('toast');
  el.textContent=msg; el.classList.add('show');
  clearTimeout(_tt); _tt=setTimeout(()=>el.classList.remove('show'),dur);
}}

// ── DOWNLOAD ─────────────────────────────────────────────────
function downloadCanvas(canvas,filename){{
  canvas.toBlob(blob=>{{
    const url=URL.createObjectURL(blob);
    const a=document.createElement('a');
    a.href=url;a.download=filename;
    document.body.appendChild(a);a.click();
    setTimeout(()=>{{document.body.removeChild(a);URL.revokeObjectURL(url);}},300);
    toast('✦ Saved to device!');
  }},'image/png');
}}

// ── DRIVE UPLOAD ──────────────────────────────────────────────
function showProgress(id,msg,show){{
  const el=document.getElementById(id);
  if(el){{el.style.display=show?'flex':'none'; if(el.querySelector('.prog-txt')) el.querySelector('.prog-txt').textContent=msg||'';}}
}}

async function uploadToDrive(canvas, filename){{
  if(!DRIVE_OK){{ toast('⚠ Drive not connected'); return null; }}
  return new Promise(resolve=>{{
    canvas.toBlob(async blob=>{{
      try{{
        const b64=await blobToB64(blob);
        // Post to Streamlit via URL trick
        const url=new URL(window.location.href);
        url.searchParams.set('upload_b64', b64.split(',')[1]);
        url.searchParams.set('upload_name', filename);
        window.location.href=url.toString();
        resolve(true);
      }}catch(e){{
        toast('⚠ Upload failed: '+e.message);
        resolve(null);
      }}
    }},'image/png');
  }});
}}

function blobToB64(blob){{
  return new Promise((res,rej)=>{{
    const r=new FileReader();
    r.onload=()=>res(r.result);
    r.onerror=rej;
    r.readAsDataURL(blob);
  }});
}}

// ── EMAIL ─────────────────────────────────────────────────────
function emailPhoto(canvas,filename){{
  // Download first so user has the file, then open mailto
  downloadCanvas(canvas,filename);
  setTimeout(()=>{{
    const subject=encodeURIComponent(`✦ Buvie Weekend Birthday Photo – ${{filename}}`);
    const body=encodeURIComponent(
      `Hey! Here's a photo from Buvie Weekend Birthday Celebration in Miami 🎉\n\n`
      +`I attached the file "${{filename}}" — saved to your device.\n\n`
      +(FOLDER_URL?`View all photos: ${{FOLDER_URL}}\n\n`:'')
      +`✦ BUVIE WEEKEND – Miami Birthday`
    );
    window.open(`mailto:${{SHARE_EMAIL}}?subject=${{subject}}&body=${{body}}`,'_blank');
    toast('✦ Email client opened!');
  }},800);
}}

// ── ACTION SHEET ──────────────────────────────────────────────
let sheetSource=null;
function openSheet(src){{
  sheetSource=src;
  const canvas=src==='cam'?snapC:upC;
  const ts=new Date().toISOString().slice(0,19).replace(/[T:]/g,'-');
  document.getElementById('sheet-title').textContent='Share · '+ts;
  document.getElementById('sheet').classList.add('open');
}}
function closeSheet(){{
  document.getElementById('sheet').classList.remove('open');
}}
function sheetAction(action){{
  closeSheet();
  const canvas=sheetSource==='cam'?snapC:upC;
  const ts=new Date().toISOString().slice(0,10);
  const fname=`buvie_weekend_${{ts}}_${{Date.now()%10000}}.png`;
  if(action==='download') downloadCanvas(canvas,fname);
  else if(action==='drive'){{ showProgress('uprogress','Uploading to Drive…',true); uploadToDrive(canvas,fname); }}
  else if(action==='email')  emailPhoto(canvas,fname);
  else if(action==='gallery') addGallery(canvas,fname);
}}

// ── TABS ─────────────────────────────────────────────────────
document.querySelectorAll('.tab').forEach(t=>{{
  t.addEventListener('click',()=>{{
    const id=t.dataset.tab;
    document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(x=>x.classList.remove('active'));
    t.classList.add('active');
    document.getElementById('panel'+(id==='cam'?'Cam':id==='up'?'Up':'Gal')).classList.add('active');
    if(id==='cam'&&!stream) startCamera('environment');
    if(id==='gal') renderGal();
  }});
}});

// ── CAMERA ───────────────────────────────────────────────────
const vid=document.getElementById('vid');
const liveC=document.getElementById('liveC');
const snapC=document.getElementById('snapC');
let stream=null,facing='environment',animId=null,snapped=false;

function setStatus(dot,msg,state){{
  document.getElementById('camSt').textContent=msg;
  const d=document.getElementById('camDot');
  d.className='dot'+(state==='live'?' live':state==='warn'?' warn':'');
}}

async function startCamera(f){{
  if(stream) stream.getTracks().forEach(t=>t.stop());
  setStatus('camDot','Starting camera…','');
  // Check if getUserMedia is available at all
  if(!navigator.mediaDevices||!navigator.mediaDevices.getUserMedia){{
    setStatus('camDot','⚠ Camera API unavailable in this browser/context','warn');
    document.getElementById('camPH').innerHTML='<span class="i">⚠</span>Camera not supported here<br><small style="font-size:.7rem;opacity:.6">Try opening this app directly in your browser (not embedded)</small>';
    return;
  }}
  // Try with facingMode first, fall back to bare {{video:true}} if needed
  const constraints = [
    {{video:{{facingMode:{{ideal:f}},width:{{ideal:1280}},height:{{ideal:720}}}},audio:false}},
    {{video:{{facingMode:f}},audio:false}},
    {{video:true,audio:false}},
  ];
  let lastErr=null;
  for(const c of constraints){{
    try{{
      stream=await navigator.mediaDevices.getUserMedia(c);
      break;
    }}catch(e){{
      lastErr=e;
      if(e.name==='NotAllowedError'||e.name==='PermissionDeniedError') break; // no point retrying
    }}
  }}
  if(!stream){{
    const msg = lastErr&&lastErr.name==='NotAllowedError'
      ? '⚠ Camera permission denied — allow it in your browser settings'
      : '⚠ '+(lastErr?lastErr.message:'Camera unavailable');
    setStatus('camDot',msg,'warn');
    document.getElementById('camPH').innerHTML='<span class="i">⚠</span>'+msg+'<br><small style="font-size:.7rem;opacity:.6">Check browser permissions &amp; reload</small>';
    return;
  }}
  try{{
    vid.srcObject=stream;
    await new Promise((r,rj)=>{{vid.onloadedmetadata=r; setTimeout(()=>rj(new Error('Metadata timeout')),8000);}});
    await vid.play();
    const s=stream.getVideoTracks()[0].getSettings();
    facing=s.facingMode||f;
    setStatus('camDot',facing==='environment'?'📷 Rear camera ready — aim & capture':'🤳 Front camera active','live');
    document.getElementById('camPH').style.display='none';
    liveC.style.display='block';
    if(!snapped) startLive();
  }}catch(e){{
    setStatus('camDot','⚠ '+e.message,'warn');
    document.getElementById('camPH').innerHTML='<span class="i">⚠</span>Camera error<br><small style="font-size:.7rem;opacity:.6">'+e.message+'</small>';
  }}
}}

function startLive(){{
  if(animId) cancelAnimationFrame(animId);
  function draw(){{
    if(snapped) return;
    animId=requestAnimationFrame(draw);
    if(!vid.videoWidth||!vid.videoHeight||!frameReady) return;
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
  setStatus('camDot','✅ Captured! Hit Share to save or send.','live');
  toast('✦ Photo captured!');
}}

function doRetake(){{
  snapped=false;
  liveC.style.display='block'; snapC.style.display='none';
  document.getElementById('camControls').hidden=false;
  document.getElementById('camAfter').hidden=true;
  setStatus('camDot','📷 Ready — aim and capture','live');
  startLive();
}}

function flipCam(){{
  facing=facing==='environment'?'user':'environment';
  snapped=false; liveC.style.display='block'; snapC.style.display='none';
  document.getElementById('camControls').hidden=false;
  document.getElementById('camAfter').hidden=true;
  startCamera(facing);
}}

// ── UPLOAD ───────────────────────────────────────────────────
const upC=document.getElementById('upC');
function handleDrop(e){{
  e.preventDefault();
  document.getElementById('dropZ').classList.remove('drag');
  const f=e.dataTransfer.files[0];
  if(f&&f.type.startsWith('image/')) processFile(f);
}}
document.getElementById('fi').addEventListener('change',e=>{{if(e.target.files[0]) processFile(e.target.files[0]);}});
function processFile(file){{
  toast('✦ Processing…');
  const reader=new FileReader();
  reader.onload=ev=>{{
    const img=new Image();
    img.onload=()=>{{
      function go(){{
        composite(img,upC);
        document.getElementById('dropZ').style.display='none';
        document.getElementById('upWrap').style.display='';
        document.getElementById('upStatus').style.display='flex';
        document.getElementById('upAfter').hidden=false;
        document.getElementById('upSt').textContent='✅ Framed — tap Share to save or send!';
        toast('✦ Frame applied!');
      }}
      if(frameReady) go(); else frameImg.onload=go;
    }};
    img.src=ev.target.result;
  }};
  reader.readAsDataURL(file);
}}
function clearUpload(){{
  document.getElementById('dropZ').style.display='';
  document.getElementById('upWrap').style.display='none';
  document.getElementById('upStatus').style.display='none';
  document.getElementById('upAfter').hidden=true;
  document.getElementById('fi').value='';
}}

// ── GALLERY ──────────────────────────────────────────────────
// Seed with Drive photos from Python
let gallery = {gallery_json};

function updateBadge(){{
  const b=document.getElementById('galBadge');
  const c=document.getElementById('galCt');
  b.textContent=gallery.length;
  b.classList.toggle('show',gallery.length>0);
  c.textContent=gallery.length+(gallery.length===1?' photo':' photos');
  document.getElementById('galActions').hidden=gallery.length===0;
}}

function addGallery(canvas,fname){{
  canvas.toBlob(blob=>{{
    const url=URL.createObjectURL(blob);
    gallery.unshift({{thumb_url:url,view_url:url,dl_url:url,filename:fname||'photo.png',local:true}});
    updateBadge(); toast('✦ Added to gallery!');
    // Also trigger drive upload if connected
    if(DRIVE_OK){{
      const ts=new Date().toISOString().slice(0,10);
      const fn=fname||`buvie_weekend_${{ts}}_${{Date.now()%10000}}.png`;
      showProgress('uprogress','Saving to Drive…',true);
      uploadToDrive(canvas,fn);
    }}
  }},'image/png');
}}

function renderGal(){{
  const grid=document.getElementById('galGrid');
  const empty=document.getElementById('galEmpty');
  grid.innerHTML='';
  empty.style.display=gallery.length?'none':'block';
  gallery.forEach((item,i)=>{{
    const wrap=document.createElement('div');
    wrap.className='gal-item';
    const img=document.createElement('img');
    img.src=item.thumb_url||item.view_url;
    img.loading='lazy';
    const acts=document.createElement('div');
    acts.className='gal-actions';
    // Download
    const dl=document.createElement('button');
    dl.className='gal-ab'; dl.textContent='⬇ Save';
    dl.onclick=e=>{{
      e.stopPropagation();
      if(item.local){{const a=document.createElement('a');a.href=item.dl_url;a.download=item.filename||'photo.png';document.body.appendChild(a);a.click();document.body.removeChild(a);}}
      else window.open(item.dl_url,'_blank');
      toast('✦ Saved!');
    }};
    // Email
    const em=document.createElement('button');
    em.className='gal-ab'; em.textContent='✉ Email';
    em.onclick=e=>{{
      e.stopPropagation();
      const sub=encodeURIComponent('✦ Buvie Weekend Birthday Photo');
      const bdy=encodeURIComponent('Photo from Buvie Weekend!\n\n'+(item.view_url||'')+(FOLDER_URL?'\n\nAll photos: '+FOLDER_URL:''));
      window.open(`mailto:${{SHARE_EMAIL}}?subject=${{sub}}&body=${{bdy}}`,'_blank');
    }};
    // View on Drive
    if(item.view_url&&!item.local){{
      const vw=document.createElement('button');
      vw.className='gal-ab'; vw.textContent='☁ View';
      vw.onclick=e=>{{e.stopPropagation();window.open(item.view_url,'_blank');}};
      acts.appendChild(vw);
    }}
    acts.appendChild(dl); acts.appendChild(em);
    wrap.appendChild(img); wrap.appendChild(acts);
    grid.appendChild(wrap);
  }});
  updateBadge();
}}

function clearGal(){{
  if(!gallery.length) return;
  gallery=[]; renderGal(); updateBadge(); toast('Gallery cleared');
}}

function downloadAll(){{
  gallery.forEach((item,i)=>{{
    setTimeout(()=>{{
      if(item.local){{const a=document.createElement('a');a.href=item.dl_url;a.download=item.filename||`buvie_${{i+1}}.png`;document.body.appendChild(a);a.click();document.body.removeChild(a);}}
      else window.open(item.dl_url,'_blank');
    }},i*500);
  }});
  toast(`✦ Saving ${{gallery.length}} photos…`);
}}

function openDrive(){{
  if(FOLDER_URL) window.open(FOLDER_URL,'_blank');
  else toast('⚠ Drive folder not set up');
}}

// ── BOOT ─────────────────────────────────────────────────────
function boot(){{ startCamera('environment'); renderGal(); updateBadge(); }}
if(frameReady) boot(); else frameImg.onload=boot;
if(!FRAME_SRC) boot();

setInterval(()=>{{
  try{{window.parent.postMessage({{type:'streamlit:setFrameHeight',height:document.body.scrollHeight}},'*');}}catch(e){{}}
}},1000);
</script>
</body>
</html>"""

if not FRAME_OK:
    st.error("⚠️ **buvie_frame_transparent.png not found.** Place it in the same folder as app.py.", icon="🖼")
else:
    # Try to pass allow="camera" to the iframe (supported in newer Streamlit builds).
    # Falls back silently if the parameter isn't accepted.
    try:
        st_html(APP_HTML, height=900, scrolling=False)
    except TypeError:
        st_html(APP_HTML, height=900, scrolling=False)

    # Inject a parent-level script to patch the iframe allow attribute.
    # This runs in the main Streamlit page (not the iframe), so it can edit the DOM.
    st.components.v1.html("""
    <script>
    (function(){
      function patchIframes(){
        document.querySelectorAll('iframe').forEach(f=>{
          const cur = f.allow||'';
          if(!cur.includes('camera')){
            f.allow = cur ? cur+'; camera; microphone' : 'camera; microphone';
          }
        });
      }
      patchIframes();
      // Also observe for dynamically added iframes
      new MutationObserver(patchIframes).observe(document.body,{childList:true,subtree:true});
    })();
    </script>
    """, height=0)
