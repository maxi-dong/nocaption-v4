import streamlit as st
import os
import random
import re
import subprocess
import datetime
import ssl
import shutil
import concurrent.futures
import json
import threading

# ==========================================
# 📱 DATABASE HP (GLOBAL)
# ==========================================
# Ini harus ditaruh di luar fungsi agar bisa dibaca Sidebar UI & Worker
MOBILE_POOL_DATA = [
    # --- APPLE (iOS) ---
    {"make": "Apple", "model": "iPhone 15 Pro Max", "software": "iOS 17.4.1"},
    {"make": "Apple", "model": "iPhone 15", "software": "iOS 17.2"},
    {"make": "Apple", "model": "iPhone 14 Pro Max", "software": "iOS 16.6"},
    {"make": "Apple", "model": "iPhone 14", "software": "iOS 16.1.2"},
    {"make": "Apple", "model": "iPhone 13 Pro", "software": "iOS 15.5"},
    {"make": "Apple", "model": "iPhone 13", "software": "iOS 16.3"},
    {"make": "Apple", "model": "iPhone 12", "software": "iOS 15.4.1"},
    {"make": "Apple", "model": "iPhone 11", "software": "iOS 14.8"},
    {"make": "Apple", "model": "iPhone SE (3rd generation)", "software": "iOS 17.0"},
    # --- SAMSUNG (Android OneUI) ---
    {"make": "Samsung", "model": "SM-S928B", "software": "Android 14"}, # S24 Ultra
    {"make": "Samsung", "model": "SM-S921B", "software": "Android 14"}, # S24 Biasa
    {"make": "Samsung", "model": "SM-S918B", "software": "Android 13"}, # S23 Ultra
    {"make": "Samsung", "model": "SM-S908B", "software": "Android 12"}, # S22 Ultra
    {"make": "Samsung", "model": "SM-G998B", "software": "Android 11"}, # S21 Ultra
    {"make": "Samsung", "model": "SM-A546B", "software": "Android 13"}, # Galaxy A54
    {"make": "Samsung", "model": "SM-A536B", "software": "Android 12"}, # Galaxy A53
    {"make": "Samsung", "model": "SM-F731B", "software": "Android 13"}, # Z Flip 5
    # --- GOOGLE (Pixel) ---
    {"make": "Google", "model": "Pixel 8 Pro", "software": "Android 14"},
    {"make": "Google", "model": "Pixel 8", "software": "Android 14"},
    {"make": "Google", "model": "Pixel 7 Pro", "software": "Android 13"},
    {"make": "Google", "model": "Pixel 6a", "software": "Android 12"},
    # --- OTHER BRANDS ---
    {"make": "Xiaomi", "model": "23127PN0CG", "software": "Android 14"}, # Xiaomi 14
    {"make": "Xiaomi", "model": "2210132G", "software": "Android 13"},   # Xiaomi 13 Pro
    {"make": "OnePlus", "model": "CPH2581", "software": "Android 14"},   # OnePlus 12
    {"make": "OnePlus", "model": "CPH2449", "software": "Android 13"},   # OnePlus 11
    {"make": "OPPO", "model": "CPH2551", "software": "Android 13"},      # Find N3 Flip
    {"make": "Sony", "model": "XQ-DQ72", "software": "Android 13"}       # Xperia 1 V
]

# ==========================================
# 🎬 VIDEO EDITOR DATABASE (Anti-Detect)
# ==========================================
EDITOR_POOL = [
    "CapCut 7.0.1",
    "CapCut for Desktop",
    "KineMaster 6.0.6",
    "InShot - Video Editor",
    "Adobe Premiere Pro 2023 (23.0.0)",
    "Adobe Media Encoder 2023",
    "DaVinci Resolve 18.5",
    "Canva Video Editor",
    "Final Cut Pro 10.6.5",
    "Splice - Video Editor",
    "VN Video Editor",
    "Filmora 12.0.0"
]

# ==========================================
# 🔒 GLOBAL LOCK FOR WHISPER
# ==========================================
# Lock ini mencegah race condition saat multiple thread mengakses GPU/CPU untuk transcribe
whisper_lock = threading.Lock()

# ==========================================
# 💾 SAVE & LOAD CONFIG
# ==========================================
CONFIG_FILE = "v9_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except: return {}
    return {}

def save_config(config_data):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f)
    except: pass

saved_config = load_config()

# ==========================================
# 🛡️ GLOBAL SSL BYPASS
# ==========================================
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Video Gen Ultimate V9", layout="wide", page_icon="💎")

# ==========================================
# 🎨 UI DESIGN: GLASSMORPHISM
# ==========================================
def inject_css():
    bg_gradient = "linear-gradient(140deg, #4facfe 0%, #00f2fe 30%, #a18cd1 80%, #ff7eb3 100%)"
    glass_bg = "rgba(255, 255, 255, 0.45)"
    sidebar_bg = "rgba(255, 255, 255, 0.35)"
    glass_border = "1px solid rgba(255, 255, 255, 0.8)"
    text_color = "#2c3e50"
    accent_pink = "#ff758c"
    btn_gradient = "linear-gradient(90deg, #ff7eb3 0%, #ff758c 100%)"

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
        
        html, body, [class*="ViewContainer"], [data-testid="stAppViewContainer"], [data-testid="stApp"] {{
            background: {bg_gradient} !important;
            background-size: cover !important;
            background-attachment: fixed !important;
            color: {text_color} !important;
            font-family: 'Poppins', sans-serif !important;
        }}
        
        header[data-testid="stHeader"] {{ background: transparent !important; }}
        
        [data-testid="stSidebar"] {{
            background-color: {sidebar_bg} !important;
            backdrop-filter: blur(25px) !important;
            border-right: {glass_border} !important;
        }}
        [data-testid="stSidebar"] * {{ color: {text_color} !important; }}
        
        input[type="text"], input[type="number"], div[data-baseweb="select"] > div {{
            background-color: rgba(255, 255, 255, 0.6) !important;
            border: {glass_border} !important;
            border-radius: 50px !important;
            color: {text_color} !important;
            padding-left: 10px !important;
        }}
        input {{ color: {text_color} !important; }}
        
        div.stButton > button {{
            background: {btn_gradient} !important;
            color: white !important;
            border-radius: 50px !important;
            border: none !important;
            padding: 0.6rem 1.5rem !important;
            font-weight: 600 !important;
            box-shadow: 0 5px 15px rgba(255, 117, 140, 0.4) !important;
            transition: transform 0.2s !important;
        }}
        div.stButton > button:hover {{
            transform: scale(1.05) !important;
            box-shadow: 0 8px 20px rgba(255, 117, 140, 0.6) !important;
        }}
        
        button[kind="primary"] {{
            background: linear-gradient(90deg, #8E2DE2 0%, #4A00E0 100%) !important;
            box-shadow: 0 10px 25px rgba(74, 0, 224, 0.3) !important;
        }}

        .glass-card {{
            background: {glass_bg};
            backdrop-filter: blur(30px);
            border-radius: 30px;
            border: {glass_border};
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.05);
        }}
        
        /* Fix Sliders & Text */
        div.stSlider, div[data-baseweb="slider"] {{ width: 100% !important; }}
        .stAlert {{ background-color: rgba(255,255,255,0.8) !important; border-radius: 15px !important; }}
        </style>
    """, unsafe_allow_html=True)

inject_css()

# ==========================================
# 🧠 HELPER FUNCTIONS
# ==========================================
# Init Session State
for key in ['path_vid', 'path_vo', 'path_mus', 'path_out', 'file_intro', 'file_outro', 'path_hook', 'path_prob', 'path_sol', 'path_cta']:
    if key not in st.session_state: st.session_state[key] = saved_config.get(key, "")

@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

def pick_callback(state_key, mode="folder", title="Pilih"):
    try:
        scpt_mode = 'folder' if mode == 'folder' else 'file'
        type_filter = 'of type {"mp4", "mov", "mp3", "wav"}' if mode == 'file' else ''
        scpt = f"""tell application "System Events" 
            activate
            set f to choose {scpt_mode} with prompt "{title}" {type_filter} default location (path to home folder)
            return POSIX path of f
        end tell"""
        result = subprocess.run(['osascript', '-e', scpt], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        path = result.stdout.strip()
        if path: st.session_state[state_key] = path
    except Exception as e: print(f"Error picking: {e}")

def glass_card_start(): st.markdown('<div class="glass-card">', unsafe_allow_html=True)
def glass_card_end(): st.markdown('</div>', unsafe_allow_html=True)

def get_duration(ffmpeg_exe, file_path):
    try:
        cmd = [ffmpeg_exe, '-i', file_path, '-hide_banner']
        result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        match = re.search(r"Duration: (\d{2}):(\d{2}):(\d{2}\.\d+)", result.stderr)
        if match:
            h, m, s = map(float, match.groups())
            return h*3600 + m*60 + s
    except: pass
    return 0

def has_audio_stream(ffmpeg_exe, file_path):
    try:
        cmd = [ffmpeg_exe, '-i', file_path, '-hide_banner']
        result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        return "Audio:" in result.stderr
    except: return False

def check_media_integrity(ffmpeg_path, file_path):
    try:
        cmd = [ffmpeg_path, '-v', 'error', '-i', file_path, '-f', 'null', '-']
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except: return False

def get_files(folder, extensions):
    if not folder or not os.path.exists(folder): return []
    return [f for f in os.listdir(folder) if f.lower().endswith(extensions) and not f.startswith("._")]

def format_timestamp(seconds):
    td = datetime.timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    return f"{total_seconds//3600:02}:{(total_seconds%3600)//60:02}:{total_seconds%60:02},{int((seconds-int(seconds))*1000):03}"

def generate_srt(model, audio_path, srt_path, ffmpeg_exe):
    # Convert audio to clean 16kHz WAV for Whisper
    temp_safe_audio = srt_path.replace(".srt", "_safe.wav")
    try:
        cmd = [ffmpeg_exe, '-y', '-i', audio_path, '-ar', '16000', '-ac', '1', '-c:a', 'pcm_s16le', temp_safe_audio]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # LOCK: Wait for GPU/CPU resource
        with whisper_lock:
            result = model.transcribe(temp_safe_audio, fp16=False)
        
        with open(srt_path, "w", encoding="utf-8") as f:
            for i, s in enumerate(result["segments"]):
                f.write(f"{i+1}\n{format_timestamp(s['start'])} --> {format_timestamp(s['end'])}\n{s['text'].strip()}\n\n")      
    except Exception as e:
        print(f"Generate SRT Error: {e}")
        raise e
    finally:
        if os.path.exists(temp_safe_audio): os.remove(temp_safe_audio)
    return srt_path

def hex_to_ass(hex_c):
    h = hex_c.lstrip('#')
    return f"&H{h[4:6]}{h[2:4]}{h[0:2]}" if len(h)==6 else "&HFFFFFF"

def generate_smart_blueprints(hooks, probs, sols, ctas, limit):
    import itertools
    blueprints = []
    seen_combinations = set()
    max_possible = len(hooks) * len(probs) * len(sols) * len(ctas)
    target = min(limit, max_possible)
    attempts = 0
    max_attempts = limit * 50
    while len(blueprints) < target and attempts < max_attempts:
        h = random.choice(hooks)
        p = random.choice(probs)
        s = random.choice(sols)
        c = random.choice(ctas)
        combo_signature = (h, p, s, c)
        if combo_signature not in seen_combinations:
            seen_combinations.add(combo_signature)
            blueprints.append(combo_signature)
            attempts = 0
        else: attempts += 1
    return blueprints, max_possible

def spacer(): st.markdown('<div style="margin-top: 29px;"></div>', unsafe_allow_html=True)

# ==========================================
# ⚙️ SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("## 🎛️ Control Center")
    with st.expander("🚀 Hardware Acceleration (Render Speed)", expanded=True):
        st.caption("Pilih 'Apple Silicon' jika Anda menggunakan Mac M1/M2/M3 agar render 5x lebih cepat.")
        
        # Opsi Hardware
        hw_options = [
            "CPU (Standard - libx264) - Lambat tapi Stabil", 
            "Apple Silicon (Mac M1/M2/M3 - videotoolbox) - Super Cepat", 
            "NVIDIA GPU (Windows - nvenc) - Cepat"
        ]
        
        # Auto-Select Apple Silicon karena path Anda terdeteksi Mac
        def_idx = 0
        import platform
        if platform.system() == "Darwin" and platform.machine() == "arm64":
            def_idx = 1
            
        hw_choice = st.selectbox("Render Engine", hw_options, index=def_idx)
        target_bitrate = st.selectbox("Target Quality", ["3M (Light)", "5M (Standard)", "8M (High)"], index=1)
        
    with st.expander("⚡ Performance & Threading (Turbo Mode)", expanded=True):
        import multiprocessing
        total_cores = multiprocessing.cpu_count()
        
        st.caption(f"CPU Anda memiliki {total_cores} Core. Semakin tinggi thread, semakin cepat, tapi PC makin berat.")
        
        # Opsi Threading: Safe, Balanced, Extreme
        threads_val = st.select_slider(
            "Jumlah Video per Batch (Concurrent Workers)",
            options=[2, 4, 8, 12, 16, 20, 32],
            value=8 if total_cores >= 8 else 4,
            help="Tentukan berapa banyak video yang dirender secara bersamaan."
        )
        
    with st.expander("🔊 Audio Intelligence", expanded=False):
        use_ducking = st.toggle("Smart Ducking", value=True)
        keep_ori_audio = st.toggle("🔊 Keep Original Video Audio", value=False)
    
    with st.expander("🎬 Intro & Outro", expanded=False):
        use_intro = st.toggle("Intro", False)
        if use_intro:
            st.text_input("Intro Path", key="file_intro", label_visibility="collapsed")
            st.button("📂 Pick Intro", on_click=pick_callback, args=('file_intro', 'file', 'Pilih Intro'))
        st.divider()
        use_outro = st.toggle("Outro", False)
        if use_outro:
            st.text_input("Outro Path", key="file_outro", label_visibility="collapsed")
            st.button("📂 Pick Outro", on_click=pick_callback, args=('file_outro', 'file', 'Pilih Outro'))

    with st.expander("🔤 Title Overlay", expanded=False):
        use_title = st.toggle("Enable Title", False)
        title_text, t_font, t_size, t_color, title_y, title_full_dur, title_dur_sec = "", "Arial", 60, "#FFFFFF", "(h-text_h)/2", True, 0
        if use_title:
            title_text = st.text_input("Text", "TOP 5 FACTS")
            t_size = st.number_input("Size", 30, 200, 80)
            t_color = st.color_picker("Color", "#FFFFFF")
            t_pos = st.select_slider("Position", ["Top", "Center", "Bottom"])
            title_y = {"Top": "150", "Center": "(h-text_h)/2", "Bottom": "h-150"}[t_pos]
            title_full_dur = st.checkbox("Full Duration", value=True)
            if not title_full_dur:
                title_dur_sec = st.number_input("Show for (seconds)", 1.0, 60.0, 3.0, 0.5)

    # Caption feature removed
    use_captions = False
    style_config = {}

    with st.expander("✨ Visual Effects (Custom)", expanded=True):
        c1, c2 = st.columns([1, 3]) 
        with c1: zoom_on = st.toggle("Zoom", True); 
        with c2: zoom_val = st.slider("Scale", 1.01, 1.30, 1.05, 0.01, disabled=not zoom_on)
        c1, c2 = st.columns([1, 3])
        with c1: vig_on = st.toggle("Vignette", True); 
        with c2: vig_val = st.slider("Darkness", 0.1, 1.0, 0.3, 0.1, disabled=not vig_on)
        c1, c2 = st.columns([1, 3])
        with c1: speed_on = st.toggle("Speed", True); 
        with c2: speed_val = st.slider("Var %", 0, 20, 5, 1, disabled=not speed_on)
        c1, c2 = st.columns([1, 3])
        with c1: noise_on = st.toggle("Grain", True); 
        with c2: noise_val = st.slider("Intense", 5, 50, 12, 1, disabled=not noise_on)
        
    with st.expander("🎬 Production Settings", expanded=True):
        limit_qty = st.number_input("📊 Total Videos to Generate", 1, 5000, 5)

    with st.expander("🕵️ Metadata Spoofer (Anti-Detect)", expanded=False):
        spoof_on = st.toggle("Enable Metadata Spoofing", True)
        
        if spoof_on:
            # ==========================================
            # 1. DEVICE CONFIG (Updated Logic)
            # ==========================================
            device_presets = {
                "🎲 Random Mobile (Recommended)": "random",
                "🚫 Clean / No Metadata": "clean"
            }
            
            # Loop otomatis dari list GLOBAL (MOBILE_POOL_DATA)
            # Pastikan MOBILE_POOL_DATA sudah ada di paling atas script
            try:
                for hp in MOBILE_POOL_DATA:
                    label = f"{hp['make']} {hp['model']}"
                    device_presets[label] = hp
            except NameError:
                st.error("⚠️ MOBILE_POOL_DATA belum dipaste di atas script!")
            
            selected_label = st.selectbox("Device Signature", list(device_presets.keys()))
            selected_data = device_presets[selected_label]
			# ==========================================
            # B. EDITOR SIGNATURE (BARU! - Agar muncul di UI)
            # ==========================================
            # Opsi pertama Random, sisanya ambil dari EDITOR_POOL
            editor_options = ["🎲 Random Editor (Recommended)"] + EDITOR_POOL
            sel_editor = st.selectbox("🎬 Spoof Video Editor", editor_options)
            # ==========================================
            # 2. GEO LOCATION CONFIG (Ini yang tadi hilang)
            # ==========================================
            st.markdown("---")
            geo_options = ["None (Off)", "Random Global", "Specific Target"]
            geo_mode = st.selectbox("Geo-Location Injection", geo_options)
            
            target_lat, target_long = 0.0, 0.0
            if geo_mode == "Specific Target":
                c_geo1, c_geo2 = st.columns(2)
                target_lat = c_geo1.number_input("Lat", -90.0, 90.0, 40.7128)
                target_long = c_geo2.number_input("Long", -180.0, 180.0, -74.0060)
            
            # ==========================================
            # 3. AUTHOR CONFIG
            # ==========================================
            meta_copyright = st.text_input("Copyright/Author", "Content Creator")
            
            # ==========================================
            # 4. FINAL PACKING (Dictionary)
            # ==========================================
            meta_config = {
                'on': True,
                'preset_data': selected_data,   # Data HP
                'geo_mode': geo_mode,           # Data Geo (Sekarang sudah didefinisikan)
                'lat': target_lat,
                'long': target_long,
                'author': meta_copyright
            }
        else:
            meta_config = {'on': False}

# ==========================================
# 📺 MAIN UI
# ==========================================
st.title("💎 Generate Mass Video (GMV V9)")
st.markdown("####     Automated Mass and Bulk Video Generator ")
glass_card_start()
st.markdown("### 📂 Asset Library")
gen_mode = st.radio("💎 Generation Mode", ["Random Mix (Single Folder)", "Structured Story (Hook-Case-Sol-CTA)"], horizontal=True)
st.divider()

if gen_mode == "Random Mix (Single Folder)":
    c1, c2 = st.columns([4, 1])
    with c1: st.text_input("📁 Video Source", key="path_vid")
    with c2: spacer(); st.button("Browse Vid", on_click=pick_callback, args=('path_vid',))
    
    # Clip count settings (only for Random mode)
    st.markdown("##### ⚙️ Random Mix Settings")
    c_min, c_max = st.columns(2)
    with c_min:
        min_clip = st.number_input("🎬 Min Clips per Video", 1, 10, 3, 
                                   help="Minimum number of video clips to use per generated video")
    with c_max:
        max_clip = st.number_input("🎬 Max Clips per Video", 1, 10, 5,
                                   help="Maximum number of video clips to use per generated video")
else:
    # Structured mode: Fixed 4 clips (Hook, Problem, Solution, CTA)
    min_clip, max_clip = 4, 4  # Fixed values, not used but set for consistency
    st.markdown("#### 📖 Storyboard Folders")
    cols = st.columns([4, 1])
    with cols[0]: st.text_input("1️⃣ Hook Folder", key="path_hook")
    with cols[1]: spacer(); st.button("Pick Hook", on_click=pick_callback, args=('path_hook',))
    cols = st.columns([4, 1])
    with cols[0]: st.text_input("2️⃣ Problem Folder", key="path_prob")
    with cols[1]: spacer(); st.button("Pick Prob", on_click=pick_callback, args=('path_prob',))
    cols = st.columns([4, 1])
    with cols[0]: st.text_input("3️⃣ Solution Folder", key="path_sol")
    with cols[1]: spacer(); st.button("Pick Sol", on_click=pick_callback, args=('path_sol',))
    cols = st.columns([4, 1])
    with cols[0]: st.text_input("4️⃣ CTA Folder", key="path_cta")
    with cols[1]: spacer(); st.button("Pick CTA", on_click=pick_callback, args=('path_cta',))

st.divider()
col_tog1, col_tog2 = st.columns(2)
with col_tog1: enable_vo = st.checkbox("🎙️ Enable Voice Over", value=True)
with col_tog2: enable_music = st.checkbox("🎵 Enable Music", value=True)

dur_mode = "native"
dur_min, dur_max = 15.0, 30.0

if not enable_vo:
    use_manual_dur = st.toggle("⏱️ Force Custom Duration", value=True)
    if use_manual_dur:
        dur_mode = "custom"
        c_d1, c_d2 = st.columns(2)
        dur_min = c_d1.number_input("Min Sec", 5.0, 300.0, 15.0)
        dur_max = c_d2.number_input("Max Sec", 5.0, 300.0, 20.0)
else: dur_mode = "vo_sync"

if enable_vo:
    c3, c4 = st.columns([4, 1])
    with c3: st.text_input("🎙️ Voice Over Source", key="path_vo")
    with c4: spacer(); st.button("Browse VO", on_click=pick_callback, args=('path_vo',))

if enable_music:
    c5, c6 = st.columns([4, 1])
    with c5: st.text_input("🎵 Music Source", key="path_mus")
    with c6: spacer(); st.button("Browse MP3", on_click=pick_callback, args=('path_mus',))

st.divider()
c7, c8 = st.columns([4, 1])
with c7: st.text_input("💾 Output Destination", key="path_out")
with c8: spacer(); st.button("Set Output", on_click=pick_callback, args=('path_out',))
glass_card_end()

# ==========================================
# ⚙️ WORKER FUNCTION (FIXED)
# ==========================================
def process_single_video(data):
    i, vo_file, limit_qty, cfg, dict_videos, list_vid, list_mus, ffmpeg_path, whisper_model, fixed_combo = data
    p_out = ""
    srt = None
    
    try:
        filename_suffix = vo_file if vo_file else f"Video_{i+1}"
        p_out = os.path.join(cfg['path_out'], f"Gen_{i+1}_{filename_suffix}.mp4")
        
        # --- 1. VALIDASI VO ---
        p_vo, vo_duration_check = None, 0
        if cfg['enable_vo'] and vo_file:
            temp_path = os.path.join(cfg['path_vo'], vo_file)
            
            # CRITICAL: Validate VO file has audio stream
            if os.path.exists(temp_path) and os.path.getsize(temp_path) > 1024:
                # Check if file is valid media
                if check_media_integrity(ffmpeg_path, temp_path):
                    # Check if it has audio stream (CRITICAL!)
                    if has_audio_stream(ffmpeg_path, temp_path):
                        p_vo = temp_path
                        vo_duration_check = get_duration(ffmpeg_path, p_vo)
                    else:
                        print(f"⚠️ SKIP VO Video {i}: File exists but NO AUDIO STREAM found!")
                else:
                    print(f"⚠️ SKIP VO Video {i}: Corrupt or invalid media file.")
            else:
                print(f"⚠️ SKIP VO Video {i}: File missing or too small.")

        # Caption feature disabled
        srt = None

        # --- 3. LOGIKA DURASI & VIDEO ---
        target_clip_t = None
        current_dur_mode = cfg['dur_mode']
        if current_dur_mode == "vo_sync" and not p_vo: current_dur_mode = "native"

        if current_dur_mode == "vo_sync":
            vo_dur = vo_duration_check if vo_duration_check > 0 else 15.0
            n_div = 4 
            if cfg['mode_random']: n_div = random.randint(cfg['min_clip'], cfg['max_clip'])
            target_clip_t = vo_dur / n_div
        elif current_dur_mode == "custom":
            rand_dur = random.uniform(cfg['dur_min'], cfg['dur_max'])
            n_div = 4
            if cfg['mode_random']: n_div = random.randint(cfg['min_clip'], cfg['max_clip'])
            target_clip_t = rand_dur / n_div

        full_path_combo = [] 
        if cfg['mode_random']:
            # --- MULAI DARI SINI (BARIS 582) ---
            if not list_vid:
                print(f"❌ Error: Folder video sumber kosong untuk video ke-{i}")
                return False
            
            n_target = 4 if not target_clip_t else int(n_div)
            if len(list_vid) >= n_target:
                raw_selection = random.sample(list_vid, n_target)
            else:
                raw_selection = random.choices(list_vid, k=n_target)
                
            full_path_combo = [os.path.join(cfg['path_vid'], v) for v in raw_selection]
        else:
            if fixed_combo:
                full_path_combo = [
                    os.path.join(cfg['path_hook'], fixed_combo[0]),
                    os.path.join(cfg['path_prob'], fixed_combo[1]),
                    os.path.join(cfg['path_sol'], fixed_combo[2]),
                    os.path.join(cfg['path_cta'], fixed_combo[3])
                ]
            else: 
                return False

        # Cek apakah folder music kosong sebelum memilih
        mus = None
        if cfg['enable_music'] and list_mus:
            mus = random.choice(list_mus)

        # --- 4. PEMBUATAN VISUAL (FFmpeg Filter) ---
        inputs, fc = [], ""
        W, H = 720, 1280
        
        for v_path in full_path_combo:
            if target_clip_t: inputs.extend(['-stream_loop', '-1', '-i', v_path])
            else: inputs.extend(['-i', v_path])
        
        # CRITICAL FIX: Counter starts AFTER video clips
        ctr = len(full_path_combo)
        
        print(f"DEBUG: full_path_combo has {len(full_path_combo)} clips")
        print(f"DEBUG: ctr initialized to {ctr}")
        
        concat_inputs = "" 
        n_clips_actual = len(full_path_combo)
        
        for k in range(n_clips_actual):
            current_file_dur = get_duration(ffmpeg_path, full_path_combo[k])
            final_dur = target_clip_t if target_clip_t else current_file_dur
            if not final_dur: final_dur = 5.0
            
            speed_mod = 1.0
            if cfg['fx']['speed']:
                var = cfg['fx']['speed_val'] / 100.0
                speed_mod = round(random.uniform(1.0 - var, 1.0 + var), 2)
            
            # VIDEO PROCESSING
            f_clip = f"[{k}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"
            if target_clip_t: f_clip += f",trim=duration={final_dur}"
            f_clip += f",setpts=PTS/{speed_mod}[v{k}];"
            fc += f_clip

            # AUDIO PROCESSING
            has_ori_audio = False
            if cfg['keep_ori_audio']:
                has_ori_audio = has_audio_stream(ffmpeg_path, full_path_combo[k])

            if has_ori_audio:
                speed_safe = max(0.5, min(2.0, speed_mod)) 
                f_audio = f"[{k}:a]"
                if target_clip_t: f_audio += f"atrim=duration={final_dur},"
                f_audio += f"atempo={speed_safe},volume=0.3,aformat=channel_layouts=stereo,aresample=44100[a{k}];"
                fc += f_audio
            else:
                dur_cmd = f"duration={final_dur}"
                fc += f"anullsrc=channel_layout=stereo:sample_rate=44100,atrim={dur_cmd},aformat=channel_layouts=stereo,aresample=44100[a{k}];"
            
            concat_inputs += f"[v{k}][a{k}]"
        
        # Concat Visuals
        fc += f"{concat_inputs}concat=n={n_clips_actual}:v=1:a=1:unsafe=1[base_vid][base_aud];"
        last_vid = "[base_vid]"
        
        # Visual Effects
        if cfg['fx']['zoom']: 
            z = cfg['fx']['zoom_val']
            fc += f"{last_vid}crop=w=iw/{z}:h=ih/{z}:x=(iw-ow)/2:y=(ih-oh)/2,scale={W}:{H}[v1];"; last_vid="[v1]"
        if cfg['fx']['vig']: 
            v_val = cfg['fx']['vig_val']
            fc += f"{last_vid}vignette={v_val}[v2];"; last_vid="[v2]"
        if cfg['fx']['noise']:
            n_val = cfg['fx']['noise_val']
            fc += f"{last_vid}noise=alls={n_val}:allf=t[v_noise];"; last_vid="[v_noise]"
        
        # Title Overlay
        if cfg['use_title']:
            txt = cfg['title_text'].replace(":","\\:")
            enable_cmd = ""
            if not cfg['title_full_dur']: enable_cmd = f":enable='between(t,0,{cfg['title_dur_sec']})'"
            font_path = "/System/Library/Fonts/Helvetica.ttc" if os.path.exists("/System/Library/Fonts/Helvetica.ttc") else "Arial"
            fc += f"{last_vid}drawtext=fontfile='{font_path}':text='{txt}':fontsize={cfg['t_size']}:fontcolor={cfg['t_color']}:box=1:boxcolor=black@0.5:boxborderw=10:x=(w-text_w)/2:y={cfg['title_y']}{enable_cmd}[v3];"; last_vid="[v3]"
            
        # Caption feature removed - no subtitle rendering

        # --- CRITICAL FIX: ADD VO TO INPUTS FIRST (before intro/outro) ---
        # This ensures VO index is calculated correctly
        vo_added_at_index = None
        if cfg['enable_vo'] and p_vo:
            print(f"DEBUG: Adding VO at index {ctr}, path: {p_vo}")
            inputs.extend(['-i', p_vo])
            vo_added_at_index = ctr
            ctr += 1
            print(f"DEBUG: VO added at index {vo_added_at_index}, ctr now = {ctr}")

        # Intro/Outro Handling
        fin_cat, n_cat = "", 1
        if cfg['use_intro'] and os.path.exists(cfg['file_intro']):
            inputs.extend(['-i', cfg['file_intro']]); idx_in = ctr; ctr+=1
            fc += f"[{idx_in}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1[vin];"; fin_cat+="[vin]"; n_cat+=1
        fin_cat += last_vid
        if cfg['use_outro'] and os.path.exists(cfg['file_outro']):
            inputs.extend(['-i', cfg['file_outro']]); idx_out = ctr; ctr+=1
            fc += f"[{idx_out}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1[vout];"; fin_cat+="[vout]"; n_cat+=1
        if n_cat > 1: fc += f"{fin_cat}concat=n={n_cat}:v=1:a=0[vfin];"; last_vid="[vfin]"

        # --- 5. AUDIO MIXING (FIXED INTRO_MS) ---
        # BAGIAN YANG DIPERBAIKI: MENGHITUNG DURASI INTRO SEBELUM AUDIO MIXING
        intro_ms = 0
        if cfg['use_intro'] and os.path.exists(cfg['file_intro']):
            d_in = get_duration(ffmpeg_path, cfg['file_intro'])
            if d_in: intro_ms = int(d_in * 1000)

        audio_mix_inputs = ["[base_aud]"]
        
        if vo_added_at_index is not None:
            # VO already added to inputs above, now add to filter
            idx_vo = vo_added_at_index
            print(f"DEBUG: Creating VO filter with index {idx_vo}")
            dly = f"adelay={intro_ms}|{intro_ms}" if intro_ms>0 else "anull"
            fc += f"[{idx_vo}:a]{dly},aresample=44100,aformat=channel_layouts=stereo[avo];"
            audio_mix_inputs.append("[avo]")
            
        if cfg['enable_music'] and mus:
            inputs.extend(['-stream_loop', '-1', '-i', os.path.join(cfg['path_mus'], mus)]); idx_mus = ctr; ctr+=1
            dly = f"adelay={intro_ms}|{intro_ms}" if intro_ms>0 else "anull"
            fc += f"[{idx_mus}:a]{dly},volume=0.2,aresample=44100,aformat=channel_layouts=stereo[amus];"
            audio_mix_inputs.append("[amus]")
            
        n_mix = len(audio_mix_inputs)
        mix_str = "".join(audio_mix_inputs)
        
        if cfg['use_ducking'] and "[avo]" in audio_mix_inputs and "[amus]" in audio_mix_inputs:
             fc += f"[amus][avo]sidechaincompress=threshold=0.05:ratio=10:attack=5:release=300[mduck];"
             # Gunakan afin di sini
             fc += f"[base_aud][mduck][avo]amix=inputs=3:duration=shortest[afin]" 
        else:
             fc += f"{mix_str}amix=inputs={n_mix}:duration=shortest[afin]"

        # --- 6. METADATA SETUP ---
        days_back = random.randint(1, 30)
        seconds_back = random.randint(0, 86400)
        fake_time = datetime.datetime.now() - datetime.timedelta(days=days_back, seconds=seconds_back)
        creation_time_str = fake_time.strftime('%Y-%m-%d %H:%M:%S')
        clean_title = filename_suffix.replace("_", " ").replace(".mp3", "").title()

        metadata_flags = [
            '-metadata', f'creation_time={creation_time_str}',
            '-metadata', f'title={clean_title}'
        ]

        if cfg['meta']['on']:
            m = cfg['meta']
            dev = {}
            # Device Logic
            preset_data = m.get('preset_data', 'random')
            if preset_data == "random":
                dev = random.choice(MOBILE_POOL_DATA)
            elif preset_data == "clean":
                dev = {} 
            else:
                dev = preset_data
            if dev:
                metadata_flags.extend([
                    '-metadata', f'make={dev.get("make","")}',
                    '-metadata', f'model={dev.get("model","")}',
                    '-metadata', f'software={dev.get("software","")}'
                ])
            # Editor Logic
            target_ed = m.get('target_editor', "🎲 Random Editor (Recommended)")
            fake_editor = ""
            if "Random" in target_ed:
                fake_editor = random.choice(EDITOR_POOL)
            else:
                fake_editor = target_ed
            metadata_flags.extend([
                '-metadata', f'encoder={fake_editor}',
                '-metadata', f'tool={fake_editor}',
                '-metadata', f'writing_application={fake_editor}'
            ])
            # Author & Geo
            if m.get('author'):
                metadata_flags.extend(['-metadata', f'artist={m["author"]}', '-metadata', f'copyright={m["author"]}'])
            if m.get('geo_mode') in ["Specific Target", "Random Global"]:
                lat, lng = 0.0, 0.0
                if m['geo_mode'] == "Specific Target":
                    lat, lng = m['lat'], m['long']
                else:
                    lat, lng = random.uniform(-50, 60), random.uniform(-120, 140)
                loc_str = f"{lat:+.4f}{lng:+.4f}/"
                metadata_flags.extend(['-metadata', f'location={loc_str}', '-metadata', f'location-eng={loc_str}'])
        else:
            metadata_flags.extend(['-metadata', 'encoder=iPhone Upload'])

        # --- 7. HARDWARE ACCELERATION LOGIC ---
        bitrate_val = "5000k"
        if "3M" in cfg.get('bitrate_mode', ''): bitrate_val = "3000k"
        elif "8M" in cfg.get('bitrate_mode', ''): bitrate_val = "8000k"

        accel_mode = cfg.get('hw_accel', 'CPU')
        encoding_flags = []

        if "Apple Silicon" in accel_mode:
            encoding_flags = ['-c:v', 'h264_videotoolbox', '-b:v', bitrate_val, '-allow_sw', '1']
        elif "NVIDIA" in accel_mode:
            encoding_flags = ['-c:v', 'h264_nvenc', '-preset', 'p4', '-rc', 'vbr', '-cq', '24', '-b:v', bitrate_val]
        else:
            encoding_flags = ['-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '23']

        # --- 8. FINAL COMMAND ---
        fc = fc.strip(';') 
        
        cmd = [ffmpeg_path, '-y'] + inputs + ['-filter_complex', fc, '-map', last_vid, '-map', '[afin]']
        cmd += ['-c:a', 'aac', '-b:a', '128k', '-ac', '2', '-ar', '44100']
        cmd += metadata_flags
        cmd += ['-shortest'] + encoding_flags + ['-pix_fmt', 'yuv420p', p_out]
        
        # DEBUG: Print full command
        print(f"\n{'='*80}")
        print(f"DEBUG VIDEO {i} - FULL FFMPEG COMMAND:")
        print(f"{'='*80}")
        print(" ".join(cmd))
        print(f"{'='*80}")
        print(f"FILTER COMPLEX:")
        print(f"{'='*80}")
        print(fc)
        print(f"{'='*80}\n")
        
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
        
        # Spoof Time
        ts = fake_time.timestamp()
        if os.path.exists(p_out): os.utime(p_out, (ts, ts))
        # if srt and os.path.exists(srt): os.remove(srt)
        
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg Error Video {i}: {e.stderr.decode('utf-8', errors='ignore')[-300:]}")
        return False
    except Exception as e:
        print(f"General Error {i}: {e}")
        return False

# ==========================================
# 🏁 ACTION UI (PREVIEW & LAUNCH)
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)

# Container untuk membagi tombol menjadi dua kolom (Kiri: Preview, Kanan: Launch)
col_btn1, col_btn2 = st.columns([1, 2])

# ==========================================
# 👁️ TOMBOL 1: PREVIEW (Test Cepat)
# ==========================================
with col_btn1:
    if st.button("👁️ PREVIEW (Test 1 Video)", type="secondary"):
        
        # --- 1. CEK FFMPEG ---
        possible_paths = [
            shutil.which("ffmpeg"),
            "/opt/homebrew/bin/ffmpeg",
            "/usr/local/bin/ffmpeg",
            "/Users/maxidong/Documents/ffmpeg",
            "ffmpeg"
        ]
        ffmpeg_path = next((p for p in possible_paths if p and os.path.exists(p) and os.access(p, os.X_OK)), None)
        
        if not ffmpeg_path: 
            st.error("FFmpeg not found! Pastikan path '/Users/maxidong/Documents/ffmpeg' benar.")
            st.stop()
        else: 
            os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)
        
        # --- 2. Validasi Folder Output ---
        if not st.session_state['path_out']: 
            st.error("Output folder required!"); st.stop()
        
        # --- 3. Setup Config Khusus Preview ---
        mode_random = (gen_mode == "Random Mix (Single Folder)")
        
        sample_vo = None
        if enable_vo:
            vos = get_files(st.session_state['path_vo'], ('.mp3','.wav'))
            if vos:
                sample_vo = random.choice(vos)
            else:
                st.error("Folder VO kosong!")
                st.stop()
        
        list_vid = []
        if mode_random:
            list_vid = get_files(st.session_state['path_vid'], ('.mp4','.mov'))
        
        list_mus = get_files(st.session_state['path_mus'], ('.mp3','.wav')) if enable_music else []

        cfg_prev = {
            'path_vid': st.session_state['path_vid'], 'path_vo': st.session_state['path_vo'],
            'path_mus': st.session_state['path_mus'], 'path_out': st.session_state['path_out'],
            'path_hook': st.session_state['path_hook'], 'path_prob': st.session_state['path_prob'],
            'path_sol': st.session_state['path_sol'], 'path_cta': st.session_state['path_cta'],
            'file_intro': st.session_state['file_intro'], 'file_outro': st.session_state['file_outro'],
            'mode_random': mode_random, 'enable_vo': enable_vo, 'enable_music': enable_music,
            'keep_ori_audio': keep_ori_audio, 'dur_mode': dur_mode, 'dur_min': dur_min, 'dur_max': dur_max,
            'min_clip': min_clip, 'max_clip': max_clip, 'use_intro': use_intro, 'use_outro': use_outro,
            'use_ducking': use_ducking, 'use_title': use_title, 'title_text': title_text, 't_size': t_size, 
            't_color': t_color, 'title_y': title_y, 'title_full_dur': title_full_dur, 'title_dur_sec': title_dur_sec,
            'fx': {'speed': speed_on, 'speed_val': speed_val, 'zoom': zoom_on, 'zoom_val': zoom_val, 
                   'vig': vig_on, 'vig_val': vig_val, 'noise': noise_on, 'noise_val': noise_val},
            'hw_accel': hw_choice, 'bitrate_mode': target_bitrate,
            'meta': {'on': False},
            'preview_mode': True
        }

        fixed_combo = None
        if not mode_random:
            try:
                h = random.choice(get_files(cfg_prev['path_hook'], ('.mp4','.mov')))
                p = random.choice(get_files(cfg_prev['path_prob'], ('.mp4','.mov')))
                s = random.choice(get_files(cfg_prev['path_sol'], ('.mp4','.mov')))
                c = random.choice(get_files(cfg_prev['path_cta'], ('.mp4','.mov')))
                fixed_combo = (h, p, s, c)
            except:
                st.error("Folder structure empty! Pastikan semua folder terisi video."); st.stop()

        w_model = None

        with st.spinner("⚡ Rendering Quick Preview (Max 10s)..."):
            data_pack = (0, sample_vo, 1, cfg_prev, {}, list_vid, list_mus, ffmpeg_path, w_model, fixed_combo)
            success = process_single_video(data_pack)
        
        if success:
            st.success("✅ Preview Ready!")
            # Ambil file terbaru di folder output untuk ditampilkan
            files = [os.path.join(cfg_prev['path_out'], f) for f in os.listdir(cfg_prev['path_out']) if f.endswith(".mp4")]
            if files:
                latest_vid = max(files, key=os.path.getctime)
                st.video(latest_vid)
        else:
            st.error("❌ Preview Failed. Cek Terminal untuk detail error.")

# ==========================================
# 🚀 TOMBOL 2: LAUNCH PRODUCTION (FULL)
# ==========================================
with col_btn2:
    if st.button("🚀 LAUNCH PRODUCTION (SMART)", type="primary"):
        save_config({
            'path_vid': st.session_state['path_vid'], 'path_vo': st.session_state['path_vo'],
            'path_mus': st.session_state['path_mus'], 'path_out': st.session_state['path_out'],
            'path_hook': st.session_state['path_hook'], 'path_prob': st.session_state['path_prob'],
            'path_sol': st.session_state['path_sol'], 'path_cta': st.session_state['path_cta'],
            'file_intro': st.session_state['file_intro'], 'file_outro': st.session_state['file_outro']
        })

        possible_paths = [
            shutil.which("ffmpeg"),
            "/opt/homebrew/bin/ffmpeg",
            "/usr/local/bin/ffmpeg",
            "/Users/maxidong/Documents/ffmpeg",
            "ffmpeg"
        ]
        ffmpeg_path = next((p for p in possible_paths if p and os.path.exists(p) and os.access(p, os.X_OK)), None)
        
        if not ffmpeg_path: 
            st.error("FFmpeg not found!"); st.stop()
        else: 
            os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)

        mode_random = (gen_mode == "Random Mix (Single Folder)")
        valid = True
        if mode_random:
            if not st.session_state['path_vid']: valid = False
        else:
            if not all([st.session_state['path_hook'], st.session_state['path_prob'], st.session_state['path_sol'], st.session_state['path_cta']]):
                valid = False    
        if enable_vo and not st.session_state['path_vo']: valid = False
        if enable_music and not st.session_state['path_mus']: valid = False
        if not st.session_state['path_out']: valid = False

        if not valid: 
            st.error("⚠️ Please map all enabled folders."); st.stop()

        cfg = {
            'path_vid': st.session_state['path_vid'], 'path_vo': st.session_state['path_vo'],
            'path_mus': st.session_state['path_mus'], 'path_out': st.session_state['path_out'],
            'path_hook': st.session_state['path_hook'], 'path_prob': st.session_state['path_prob'],
            'path_sol': st.session_state['path_sol'], 'path_cta': st.session_state['path_cta'],
            'file_intro': st.session_state['file_intro'], 'file_outro': st.session_state['file_outro'],
            'mode_random': mode_random, 'enable_vo': enable_vo, 'enable_music': enable_music,
            'keep_ori_audio': keep_ori_audio, 'dur_mode': dur_mode, 'dur_min': dur_min, 'dur_max': dur_max,
            'min_clip': min_clip, 'max_clip': max_clip, 'use_intro': use_intro, 'use_outro': use_outro,
            'use_ducking': use_ducking, 'use_title': use_title, 'title_text': title_text, 't_size': t_size, 
            't_color': t_color, 'title_y': title_y, 'title_full_dur': title_full_dur, 'title_dur_sec': title_dur_sec,
            'fx': {'speed': speed_on, 'speed_val': speed_val, 'zoom': zoom_on, 'zoom_val': zoom_val, 
                'vig': vig_on, 'vig_val': vig_val, 'noise': noise_on, 'noise_val': noise_val},
            'hw_accel': hw_choice, 'bitrate_mode': target_bitrate,
            'meta': meta_config,
            'preview_mode': False
        }

        list_vo = get_files(cfg['path_vo'], ('.mp3','.wav')) if enable_vo else []
        list_mus = get_files(cfg['path_mus'], ('.mp3','.wav')) if enable_music else []
        list_vid, blueprints = [], []
        
        if cfg['mode_random']:
            list_vid = get_files(cfg['path_vid'], ('.mp4','.mov'))
            if not list_vid: st.error("Video folder empty"); st.stop()
            blueprints = [None] * limit_qty
        else:
            fh = get_files(cfg['path_hook'], ('.mp4','.mov'))
            fp = get_files(cfg['path_prob'], ('.mp4','.mov'))
            fs = get_files(cfg['path_sol'], ('.mp4','.mov'))
            fc = get_files(cfg['path_cta'], ('.mp4','.mov'))
            if not (fh and fp and fs and fc):
                st.error("Structured folders incomplete!"); st.stop()
            with st.spinner("🤖 Calculating Combinations..."):
                blueprints, max_possibilities = generate_smart_blueprints(fh, fp, fs, fc, limit_qty)
            st.info(f"📊 Found {len(blueprints)} UNIQUE combinations.")
            
        final_limit = len(blueprints)
        loop_vo = []
        
        if enable_vo:
            pool_vo = list_vo.copy()
            random.shuffle(pool_vo)
            while len(pool_vo) < final_limit: pool_vo.extend(list_vo.copy())
            loop_vo = pool_vo[:final_limit]
        else:
            loop_vo = [None] * final_limit

        whisper_model = None

        jobs_data = []
        for i in range(final_limit):
            jobs_data.append((i, loop_vo[i], final_limit, cfg, {}, list_vid, list_mus, ffmpeg_path, None, blueprints[i]))

        st.markdown(f"### ⚡️ Phase 2: Rendering {final_limit} Videos...")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        completed = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads_val) as executor:
            futures = [executor.submit(process_single_video, d) for d in jobs_data]
            for future in concurrent.futures.as_completed(futures):
                if future.result(): completed += 1
                progress_bar.progress(int((completed/final_limit)*100))
                status_text.text(f"✅ Completed: {completed}/{final_limit}")

        st.balloons()
        st.success(f"🎉 RENDER SELESAI! {completed} Video berhasil dibuat.")