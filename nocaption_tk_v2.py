import os
import math
import sys
import json
import random
import re
import shutil
import datetime
import threading
import queue
import subprocess
import concurrent.futures
from pathlib import Path

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser

# ==========================================
# 📱 DATABASE HP (GLOBAL)
# ==========================================
MOBILE_POOL_DATA = [
    {"make": "Apple", "model": "iPhone 15 Pro Max", "software": "iOS 17.4.1"},
    {"make": "Apple", "model": "iPhone 15", "software": "iOS 17.2"},
    {"make": "Apple", "model": "iPhone 14 Pro Max", "software": "iOS 16.6"},
    {"make": "Apple", "model": "iPhone 14", "software": "iOS 16.1.2"},
    {"make": "Apple", "model": "iPhone 13 Pro", "software": "iOS 15.5"},
    {"make": "Apple", "model": "iPhone 13", "software": "iOS 16.3"},
    {"make": "Apple", "model": "iPhone 12", "software": "iOS 15.4.1"},
    {"make": "Apple", "model": "iPhone 11", "software": "iOS 14.8"},
    {"make": "Apple", "model": "iPhone SE (3rd generation)", "software": "iOS 17.0"},
    {"make": "Samsung", "model": "SM-S928B", "software": "Android 14"},
    {"make": "Samsung", "model": "SM-S921B", "software": "Android 14"},
    {"make": "Samsung", "model": "SM-S918B", "software": "Android 13"},
    {"make": "Samsung", "model": "SM-S908B", "software": "Android 12"},
    {"make": "Samsung", "model": "SM-G998B", "software": "Android 11"},
    {"make": "Samsung", "model": "SM-A546B", "software": "Android 13"},
    {"make": "Samsung", "model": "SM-A536B", "software": "Android 12"},
    {"make": "Samsung", "model": "SM-F731B", "software": "Android 13"},
    {"make": "Google", "model": "Pixel 8 Pro", "software": "Android 14"},
    {"make": "Google", "model": "Pixel 8", "software": "Android 14"},
    {"make": "Google", "model": "Pixel 7 Pro", "software": "Android 13"},
    {"make": "Google", "model": "Pixel 6a", "software": "Android 12"},
    {"make": "Xiaomi", "model": "23127PN0CG", "software": "Android 14"},
    {"make": "Xiaomi", "model": "2210132G", "software": "Android 13"},
    {"make": "OnePlus", "model": "CPH2581", "software": "Android 14"},
    {"make": "OnePlus", "model": "CPH2449", "software": "Android 13"},
    {"make": "OPPO", "model": "CPH2551", "software": "Android 13"},
    {"make": "Sony", "model": "XQ-DQ72", "software": "Android 13"}
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
# 💾 SAVE & LOAD CONFIG
# ==========================================
APP_DATA_DIR = Path.home() / "Documents" / "NOCAPTION_V2"
APP_DATA_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_FILE = APP_DATA_DIR / "v9_config.json"


def load_config():
    if CONFIG_FILE.exists():
        try:
            with CONFIG_FILE.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_config(config_data):
    try:
        with CONFIG_FILE.open("w", encoding="utf-8") as f:
            json.dump(config_data, f)
    except Exception:
        pass


# ==========================================
# 🧠 HELPER FUNCTIONS
# ==========================================

def get_duration(ffmpeg_exe, file_path):
    try:
        cmd = [ffmpeg_exe, '-i', file_path, '-hide_banner']
        result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        match = re.search(r"Duration: (\d{2}):(\d{2}):(\d{2}\.\d+)", result.stderr)
        if match:
            h, m, s = map(float, match.groups())
            return h * 3600 + m * 60 + s
    except Exception:
        pass
    return 0


def has_audio_stream(ffmpeg_exe, file_path):
    try:
        cmd = [ffmpeg_exe, '-i', file_path, '-hide_banner']
        result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        return "Audio:" in result.stderr
    except Exception:
        return False


def check_media_integrity(ffmpeg_path, file_path):
    try:
        cmd = [ffmpeg_path, '-v', 'error', '-i', file_path, '-f', 'null', '-']
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception:
        return False


def get_files(folder, extensions):
    if not folder or not os.path.exists(folder):
        return []
    return [f for f in os.listdir(folder) if f.lower().endswith(extensions) and not f.startswith("._")]


def generate_smart_blueprints(hooks, probs, sols, ctas, limit):
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
        else:
            attempts += 1
    return blueprints, max_possible

def generate_structured_blueprints(hooks, probs, sols, ctas, outros, limit):
    blueprints = []
    seen_combinations = set()
    max_possible = len(hooks) * len(probs) * len(sols) * len(ctas) * len(outros)
    target = min(limit, max_possible)
    attempts = 0
    max_attempts = limit * 50

    while len(blueprints) < target and attempts < max_attempts:
        combo = (
            random.choice(hooks),
            random.choice(probs),
            random.choice(sols),
            random.choice(ctas),
            random.choice(outros),
        )
        if combo not in seen_combinations:
            seen_combinations.add(combo)
            blueprints.append(combo)
            attempts = 0
        else:
            attempts += 1
    return blueprints, max_possible


def find_ffmpeg():
    possible_paths = [
        shutil.which("ffmpeg"),
        "/opt/homebrew/bin/ffmpeg",
        "/usr/local/bin/ffmpeg",
        "/Users/maxidong/Documents/ffmpeg",
        "ffmpeg"
    ]
    return next((p for p in possible_paths if p and os.path.exists(p) and os.access(p, os.X_OK)), None)

def perm_count(n, k):
    if k < 0 or n < 0:
        return 0
    if k > n:
        return 0
    return math.perm(n, k) if hasattr(math, "perm") else math.factorial(n) // math.factorial(n - k)


def process_single_video(data, log_fn=None):
    i, vo_file, limit_qty, cfg, dict_videos, list_vid, list_mus, ffmpeg_path, fixed_combo = data
    p_out = ""

    try:
        filename_suffix = vo_file if vo_file else f"Video_{i + 1}"
        p_out = os.path.join(cfg['path_out'], f"Gen_{i + 1}_{filename_suffix}.mp4")

        # --- 1. VALIDASI VO ---
        p_vo, vo_duration_check = None, 0
        if cfg['enable_vo'] and vo_file:
            temp_path = os.path.join(cfg['path_vo'], vo_file)

            if os.path.exists(temp_path) and os.path.getsize(temp_path) > 1024:
                if check_media_integrity(ffmpeg_path, temp_path):
                    if has_audio_stream(ffmpeg_path, temp_path):
                        p_vo = temp_path
                        vo_duration_check = get_duration(ffmpeg_path, p_vo)
                    else:
                        if log_fn:
                            log_fn(f"⚠️ SKIP VO Video {i}: File exists but NO AUDIO STREAM found!")
                else:
                    if log_fn:
                        log_fn(f"⚠️ SKIP VO Video {i}: Corrupt or invalid media file.")
            else:
                if log_fn:
                    log_fn(f"⚠️ SKIP VO Video {i}: File missing or too small.")

        # --- 3. LOGIKA DURASI & VIDEO ---
        target_clip_t = None
        current_dur_mode = cfg['dur_mode']
        if current_dur_mode == "vo_sync" and not p_vo:
            current_dur_mode = "native"

        if current_dur_mode == "vo_sync":
            vo_dur = vo_duration_check if vo_duration_check > 0 else 15.0
            n_div = 4
            if cfg['mode_random']:
                n_div = random.randint(cfg['min_clip'], cfg['max_clip'])
            target_clip_t = vo_dur / n_div
        elif current_dur_mode == "custom":
            rand_dur = random.uniform(cfg['dur_min'], cfg['dur_max'])
            n_div = 4
            if cfg['mode_random']:
                n_div = random.randint(cfg['min_clip'], cfg['max_clip'])
            target_clip_t = rand_dur / n_div

        full_path_combo = []
        if cfg['mode_random']:
            # If fixed_combo provided, use it to avoid duplicate ordering
            if fixed_combo:
                full_path_combo = [os.path.join(cfg['path_vid'], v) for v in fixed_combo]
            else:
                if not list_vid:
                    if log_fn:
                        log_fn(f"❌ Error: Folder video sumber kosong untuk video ke-{i}")
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
                if len(fixed_combo) >= 5:
                    full_path_combo.append(os.path.join(cfg['path_struct_outro'], fixed_combo[4]))
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
            if target_clip_t:
                inputs.extend(['-stream_loop', '-1', '-i', v_path])
            else:
                inputs.extend(['-i', v_path])

        ctr = len(full_path_combo)

        concat_inputs = ""
        n_clips_actual = len(full_path_combo)

        for k in range(n_clips_actual):
            current_file_dur = get_duration(ffmpeg_path, full_path_combo[k])
            final_dur = target_clip_t if target_clip_t else current_file_dur
            if not final_dur:
                final_dur = 5.0

            speed_mod = 1.0
            if cfg['fx']['speed']:
                var = cfg['fx']['speed_val'] / 100.0
                speed_mod = round(random.uniform(1.0 - var, 1.0 + var), 2)

            f_clip = f"[{k}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"
            if target_clip_t:
                f_clip += f",trim=duration={final_dur}"
            f_clip += f",setpts=PTS/{speed_mod}[v{k}];"
            fc += f_clip

            has_ori_audio = False
            if cfg['keep_ori_audio']:
                has_ori_audio = has_audio_stream(ffmpeg_path, full_path_combo[k])

            if has_ori_audio:
                speed_safe = max(0.5, min(2.0, speed_mod))
                f_audio = f"[{k}:a]"
                if target_clip_t:
                    f_audio += f"atrim=duration={final_dur},"
                f_audio += f"atempo={speed_safe},volume=0.3,aformat=channel_layouts=stereo,aresample=44100[a{k}];"
                fc += f_audio
            else:
                dur_cmd = f"duration={final_dur}"
                fc += f"anullsrc=channel_layout=stereo:sample_rate=44100,atrim={dur_cmd},aformat=channel_layouts=stereo,aresample=44100[a{k}];"

            concat_inputs += f"[v{k}][a{k}]"

        fc += f"{concat_inputs}concat=n={n_clips_actual}:v=1:a=1:unsafe=1[base_vid][base_aud];"
        last_vid = "[base_vid]"

        if cfg['fx']['zoom']:
            z = cfg['fx']['zoom_val']
            fc += f"{last_vid}crop=w=iw/{z}:h=ih/{z}:x=(iw-ow)/2:y=(ih-oh)/2,scale={W}:{H}[v1];"
            last_vid = "[v1]"
        if cfg['fx']['vig']:
            v_val = cfg['fx']['vig_val']
            fc += f"{last_vid}vignette={v_val}[v2];"
            last_vid = "[v2]"
        if cfg['fx']['noise']:
            n_val = cfg['fx']['noise_val']
            fc += f"{last_vid}noise=alls={n_val}:allf=t[v_noise];"
            last_vid = "[v_noise]"

        if cfg['use_title']:
            txt = cfg['title_text'].replace(":", "\\:")
            enable_cmd = ""
            if not cfg['title_full_dur']:
                enable_cmd = f":enable='between(t,0,{cfg['title_dur_sec']})'"
            font_path = "/System/Library/Fonts/Helvetica.ttc" if os.path.exists("/System/Library/Fonts/Helvetica.ttc") else "Arial"
            fc += f"{last_vid}drawtext=fontfile='{font_path}':text='{txt}':fontsize={cfg['t_size']}:fontcolor={cfg['t_color']}:box=1:boxcolor=black@0.5:boxborderw=10:x=(w-text_w)/2:y={cfg['title_y']}{enable_cmd}[v3];"
            last_vid = "[v3]"

        vo_added_at_index = None
        if cfg['enable_vo'] and p_vo:
            inputs.extend(['-i', p_vo])
            vo_added_at_index = ctr
            ctr += 1

        fin_cat, n_cat = "", 1
        if cfg['use_intro'] and os.path.exists(cfg['file_intro']):
            inputs.extend(['-i', cfg['file_intro']])
            idx_in = ctr
            ctr += 1
            fc += f"[{idx_in}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1[vin];"
            fin_cat += "[vin]"
            n_cat += 1
        fin_cat += last_vid
        use_global_outro = cfg['use_outro']
        if (not cfg['mode_random']) and cfg.get('use_struct_outro'):
            # Structured outro folder is already appended in the main sequence.
            use_global_outro = False
        if use_global_outro and os.path.exists(cfg['file_outro']):
            inputs.extend(['-i', cfg['file_outro']])
            idx_out = ctr
            ctr += 1
            fc += f"[{idx_out}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1[vout];"
            fin_cat += "[vout]"
            n_cat += 1
        if n_cat > 1:
            fc += f"{fin_cat}concat=n={n_cat}:v=1:a=0[vfin];"
            last_vid = "[vfin]"

        intro_ms = 0
        if cfg['use_intro'] and os.path.exists(cfg['file_intro']):
            d_in = get_duration(ffmpeg_path, cfg['file_intro'])
            if d_in:
                intro_ms = int(d_in * 1000)

        audio_mix_inputs = ["[base_aud]"]

        if vo_added_at_index is not None:
            idx_vo = vo_added_at_index
            dly = f"adelay={intro_ms}|{intro_ms}" if intro_ms > 0 else "anull"
            fc += f"[{idx_vo}:a]{dly},aresample=44100,aformat=channel_layouts=stereo[avo];"
            audio_mix_inputs.append("[avo]")

        if cfg['enable_music'] and mus:
            inputs.extend(['-stream_loop', '-1', '-i', os.path.join(cfg['path_mus'], mus)])
            idx_mus = ctr
            ctr += 1
            dly = f"adelay={intro_ms}|{intro_ms}" if intro_ms > 0 else "anull"
            fc += f"[{idx_mus}:a]{dly},volume=0.2,aresample=44100,aformat=channel_layouts=stereo[amus];"
            audio_mix_inputs.append("[amus]")

        n_mix = len(audio_mix_inputs)
        mix_str = "".join(audio_mix_inputs)

        if cfg['use_ducking'] and "[avo]" in audio_mix_inputs and "[amus]" in audio_mix_inputs:
            fc += f"[amus][avo]sidechaincompress=threshold=0.05:ratio=10:attack=5:release=300[mduck];"
            fc += f"[base_aud][mduck][avo]amix=inputs=3:duration=shortest[afin]"
        else:
            fc += f"{mix_str}amix=inputs={n_mix}:duration=shortest[afin]"

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
            preset_data = m.get('preset_data', 'random')
            if preset_data == "random":
                dev = random.choice(MOBILE_POOL_DATA)
            elif preset_data == "clean":
                dev = {}
            else:
                dev = preset_data
            if dev:
                metadata_flags.extend([
                    '-metadata', f"make={dev.get('make', '')}",
                    '-metadata', f"model={dev.get('model', '')}",
                    '-metadata', f"software={dev.get('software', '')}"
                ])
            target_ed = m.get('target_editor', "🎲 Random Editor (Recommended)")
            fake_editor = ""
            if "Random" in target_ed:
                fake_editor = random.choice(EDITOR_POOL)
            else:
                fake_editor = target_ed
            metadata_flags.extend([
                '-metadata', f"encoder={fake_editor}",
                '-metadata', f"tool={fake_editor}",
                '-metadata', f"writing_application={fake_editor}"
            ])
            if m.get('author'):
                metadata_flags.extend(['-metadata', f"artist={m['author']}", '-metadata', f"copyright={m['author']}"])
            if m.get('geo_mode') in ["Specific Target", "Random Global"]:
                lat, lng = 0.0, 0.0
                if m['geo_mode'] == "Specific Target":
                    lat, lng = m['lat'], m['long']
                else:
                    lat, lng = random.uniform(-50, 60), random.uniform(-120, 140)
                loc_str = f"{lat:+.4f}{lng:+.4f}/"
                metadata_flags.extend(['-metadata', f"location={loc_str}", '-metadata', f"location-eng={loc_str}"])
        else:
            metadata_flags.extend(['-metadata', 'encoder=iPhone Upload'])

        bitrate_val = "5000k"
        if "3M" in cfg.get('bitrate_mode', ''):
            bitrate_val = "3000k"
        elif "8M" in cfg.get('bitrate_mode', ''):
            bitrate_val = "8000k"

        accel_mode = cfg.get('hw_accel', 'CPU')
        encoding_flags = []

        if "Apple Silicon" in accel_mode:
            encoding_flags = ['-c:v', 'h264_videotoolbox', '-b:v', bitrate_val, '-allow_sw', '1']
        elif "NVIDIA" in accel_mode:
            encoding_flags = ['-c:v', 'h264_nvenc', '-preset', 'p4', '-rc', 'vbr', '-cq', '24', '-b:v', bitrate_val]
        else:
            encoding_flags = ['-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '23']

        fc = fc.strip(';')

        cmd = [ffmpeg_path, '-y'] + inputs + ['-filter_complex', fc, '-map', last_vid, '-map', '[afin]']
        cmd += ['-c:a', 'aac', '-b:a', '128k', '-ac', '2', '-ar', '44100']
        cmd += metadata_flags
        cmd += ['-shortest'] + encoding_flags + ['-pix_fmt', 'yuv420p', p_out]

        if log_fn:
            log_fn(f"[FFMPEG] {p_out}")

        subprocess.run(cmd, check=True, stderr=subprocess.PIPE)

        ts = fake_time.timestamp()
        if os.path.exists(p_out):
            os.utime(p_out, (ts, ts))

        return True

    except subprocess.CalledProcessError as e:
        if log_fn:
            log_fn(f"❌ FFmpeg Error Video {i}: {e.stderr.decode('utf-8', errors='ignore')[-300:]}")
        return False
    except Exception as e:
        if log_fn:
            log_fn(f"General Error {i}: {e}")
        return False


# ==========================================
# 🎛️ GUI
# ==========================================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NOCAPTION - GMV V9 (V2)")
        self.geometry("1100x800")
        self.minsize(1000, 700)

        self.saved_config = load_config()
        self.log_queue = queue.Queue()
        self.ui_queue = queue.Queue()

        self._build_ui()
        self._start_log_pump()
        self._apply_saved_config()

    def _build_ui(self):
        nb = ttk.Notebook(self)
        nb.pack(fill=tk.BOTH, expand=True)

        self.tab_assets = ttk.Frame(nb)
        self.tab_control = ttk.Frame(nb)
        self.tab_meta = ttk.Frame(nb)
        self.tab_actions = ttk.Frame(nb)

        nb.add(self.tab_assets, text="Assets")
        nb.add(self.tab_control, text="Control")
        nb.add(self.tab_meta, text="Metadata")
        nb.add(self.tab_actions, text="Actions")

        self._build_assets_tab()
        self._build_control_tab()
        self._build_meta_tab()
        self._build_actions_tab()

    def _build_assets_tab(self):
        frm = self.tab_assets

        # Generation Mode
        mode_frame = ttk.LabelFrame(frm, text="Generation Mode")
        mode_frame.pack(fill=tk.X, padx=10, pady=8)
        self.gen_mode = tk.StringVar(value="Random Mix (Single Folder)")
        ttk.Radiobutton(mode_frame, text="Random Mix (Single Folder)", variable=self.gen_mode,
                        value="Random Mix (Single Folder)", command=self._toggle_mode).pack(side=tk.LEFT, padx=8)
        ttk.Radiobutton(mode_frame, text="Structured Story (Hook-Case-Sol-CTA)", variable=self.gen_mode,
                        value="Structured Story (Hook-Case-Sol-CTA)", command=self._toggle_mode).pack(side=tk.LEFT, padx=8)

        # Random mode inputs
        self.random_frame = ttk.LabelFrame(frm, text="Random Mix Settings")
        self.random_frame.pack(fill=tk.X, padx=10, pady=6)
        self.path_vid = tk.StringVar()
        self._path_row(self.random_frame, "Video Source", self.path_vid, is_dir=True)
        mm = ttk.Frame(self.random_frame)
        mm.pack(fill=tk.X, padx=6, pady=4)
        self.min_clip = tk.IntVar(value=3)
        self.max_clip = tk.IntVar(value=5)
        ttk.Label(mm, text="Min Clips").pack(side=tk.LEFT)
        ttk.Spinbox(mm, from_=1, to=10, textvariable=self.min_clip, width=5).pack(side=tk.LEFT, padx=6)
        ttk.Label(mm, text="Max Clips").pack(side=tk.LEFT, padx=6)
        ttk.Spinbox(mm, from_=1, to=10, textvariable=self.max_clip, width=5).pack(side=tk.LEFT)

        # Structured mode inputs
        self.struct_frame = ttk.LabelFrame(frm, text="Structured Storyboard")
        self.struct_frame.pack(fill=tk.X, padx=10, pady=6)
        self.path_hook = tk.StringVar()
        self.path_prob = tk.StringVar()
        self.path_sol = tk.StringVar()
        self.path_cta = tk.StringVar()
        self._path_row(self.struct_frame, "Hook Folder", self.path_hook, is_dir=True)
        self._path_row(self.struct_frame, "Problem Folder", self.path_prob, is_dir=True)
        self._path_row(self.struct_frame, "Solution Folder", self.path_sol, is_dir=True)
        self._path_row(self.struct_frame, "CTA Folder", self.path_cta, is_dir=True)
        self.use_struct_outro = tk.BooleanVar(value=False)
        self.path_struct_outro = tk.StringVar()
        self.struct_outro_row = ttk.Frame(self.struct_frame)
        self.struct_outro_row.pack(fill=tk.X, padx=10, pady=4)
        ttk.Checkbutton(
            self.struct_outro_row,
            text="Enable Structured Outro",
            variable=self.use_struct_outro,
            command=self._toggle_struct_outro
        ).pack(side=tk.LEFT)
        ttk.Label(self.struct_outro_row, text="Outro Folder", width=16).pack(side=tk.LEFT, padx=8)
        self.struct_outro_entry = ttk.Entry(self.struct_outro_row, textvariable=self.path_struct_outro)
        self.struct_outro_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)
        self.struct_outro_btn = ttk.Button(
            self.struct_outro_row,
            text="Browse",
            command=lambda: self._pick_dir(self.path_struct_outro)
        )
        self.struct_outro_btn.pack(side=tk.LEFT)

        # VO / Music / Output
        self.enable_vo = tk.BooleanVar(value=True)
        self.enable_music = tk.BooleanVar(value=True)
        togg = ttk.Frame(frm)
        togg.pack(fill=tk.X, padx=10, pady=6)
        ttk.Checkbutton(togg, text="Enable Voice Over", variable=self.enable_vo, command=self._toggle_vo).pack(side=tk.LEFT, padx=4)
        ttk.Checkbutton(togg, text="Enable Music", variable=self.enable_music, command=self._toggle_music).pack(side=tk.LEFT, padx=4)

        self.path_vo = tk.StringVar()
        self.path_mus = tk.StringVar()
        self._path_row(frm, "Voice Over Source", self.path_vo, is_dir=True)
        self._path_row(frm, "Music Source", self.path_mus, is_dir=True)

        self.path_out = tk.StringVar()
        self._path_row(frm, "Output Destination", self.path_out, is_dir=True)

        # Duration controls
        dur_frame = ttk.LabelFrame(frm, text="Duration")
        dur_frame.pack(fill=tk.X, padx=10, pady=6)
        self.force_custom_dur = tk.BooleanVar(value=True)
        ttk.Checkbutton(dur_frame, text="Force Custom Duration (when VO disabled)", variable=self.force_custom_dur,
                        command=self._toggle_duration).pack(side=tk.LEFT, padx=4)
        self.dur_min = tk.DoubleVar(value=15.0)
        self.dur_max = tk.DoubleVar(value=20.0)
        ttk.Label(dur_frame, text="Min Sec").pack(side=tk.LEFT, padx=6)
        ttk.Spinbox(dur_frame, from_=5.0, to=300.0, increment=0.5, textvariable=self.dur_min, width=8).pack(side=tk.LEFT)
        ttk.Label(dur_frame, text="Max Sec").pack(side=tk.LEFT, padx=6)
        ttk.Spinbox(dur_frame, from_=5.0, to=300.0, increment=0.5, textvariable=self.dur_max, width=8).pack(side=tk.LEFT)

        self._toggle_mode()
        self._toggle_vo()
        self._toggle_music()
        self._toggle_duration()
        self._toggle_struct_outro()

    def _build_control_tab(self):
        frm = self.tab_control

        # Hardware & bitrate
        hw_frame = ttk.LabelFrame(frm, text="Hardware Acceleration")
        hw_frame.pack(fill=tk.X, padx=10, pady=6)
        self.hw_choice = tk.StringVar()
        hw_options = [
            "CPU (Standard - libx264) - Lambat tapi Stabil",
            "Apple Silicon (Mac M1/M2/M3 - videotoolbox) - Super Cepat",
            "NVIDIA GPU (Windows - nvenc) - Cepat"
        ]
        default_hw = 0
        if sys.platform == "darwin" and os.uname().machine == "arm64":
            default_hw = 1
        self.hw_choice.set(hw_options[default_hw])
        ttk.Combobox(hw_frame, textvariable=self.hw_choice, values=hw_options, state="readonly", width=60).pack(side=tk.LEFT, padx=6)
        self.bitrate_mode = tk.StringVar(value="5M (Standard)")
        ttk.Combobox(hw_frame, textvariable=self.bitrate_mode,
                     values=["3M (Light)", "5M (Standard)", "8M (High)"], state="readonly", width=15).pack(side=tk.LEFT, padx=6)

        # Threading
        perf_frame = ttk.LabelFrame(frm, text="Performance & Threading")
        perf_frame.pack(fill=tk.X, padx=10, pady=6)
        self.threads_val = tk.IntVar(value=8)
        ttk.Label(perf_frame, text="Jumlah Video per Batch (Concurrent Workers)").pack(side=tk.LEFT, padx=6)
        ttk.Spinbox(perf_frame, from_=2, to=32, increment=2, textvariable=self.threads_val, width=6).pack(side=tk.LEFT)

        # Audio
        audio_frame = ttk.LabelFrame(frm, text="Audio Intelligence")
        audio_frame.pack(fill=tk.X, padx=10, pady=6)
        self.use_ducking = tk.BooleanVar(value=True)
        self.keep_ori_audio = tk.BooleanVar(value=False)
        ttk.Checkbutton(audio_frame, text="Smart Ducking", variable=self.use_ducking).pack(side=tk.LEFT, padx=6)
        ttk.Checkbutton(audio_frame, text="Keep Original Video Audio", variable=self.keep_ori_audio).pack(side=tk.LEFT, padx=6)

        # Intro/Outro
        io_frame = ttk.LabelFrame(frm, text="Intro & Outro")
        io_frame.pack(fill=tk.X, padx=10, pady=6)
        self.use_intro = tk.BooleanVar(value=False)
        self.use_outro = tk.BooleanVar(value=False)
        self.file_intro = tk.StringVar()
        self.file_outro = tk.StringVar()
        ttk.Checkbutton(io_frame, text="Intro", variable=self.use_intro).pack(side=tk.LEFT, padx=6)
        ttk.Button(io_frame, text="Pick Intro", command=lambda: self._pick_file(self.file_intro)).pack(side=tk.LEFT, padx=4)
        ttk.Entry(io_frame, textvariable=self.file_intro, width=40).pack(side=tk.LEFT, padx=4)
        ttk.Checkbutton(io_frame, text="Outro", variable=self.use_outro).pack(side=tk.LEFT, padx=6)
        ttk.Button(io_frame, text="Pick Outro", command=lambda: self._pick_file(self.file_outro)).pack(side=tk.LEFT, padx=4)
        ttk.Entry(io_frame, textvariable=self.file_outro, width=40).pack(side=tk.LEFT, padx=4)

        # Title
        title_frame = ttk.LabelFrame(frm, text="Title Overlay")
        title_frame.pack(fill=tk.X, padx=10, pady=6)
        self.use_title = tk.BooleanVar(value=False)
        self.title_text = tk.StringVar(value="TOP 5 FACTS")
        self.t_size = tk.IntVar(value=80)
        self.t_color = tk.StringVar(value="#FFFFFF")
        self.t_pos = tk.StringVar(value="Center")
        self.title_full_dur = tk.BooleanVar(value=True)
        self.title_dur_sec = tk.DoubleVar(value=3.0)
        ttk.Checkbutton(title_frame, text="Enable Title", variable=self.use_title).pack(side=tk.LEFT, padx=6)
        ttk.Entry(title_frame, textvariable=self.title_text, width=20).pack(side=tk.LEFT, padx=6)
        ttk.Spinbox(title_frame, from_=30, to=200, textvariable=self.t_size, width=6).pack(side=tk.LEFT, padx=6)
        ttk.Button(title_frame, text="Color", command=self._pick_color).pack(side=tk.LEFT, padx=6)
        ttk.Combobox(title_frame, textvariable=self.t_pos, values=["Top", "Center", "Bottom"], state="readonly", width=8).pack(side=tk.LEFT, padx=6)
        ttk.Checkbutton(title_frame, text="Full Duration", variable=self.title_full_dur).pack(side=tk.LEFT, padx=6)
        ttk.Spinbox(title_frame, from_=1.0, to=60.0, increment=0.5, textvariable=self.title_dur_sec, width=6).pack(side=tk.LEFT, padx=6)

        # Effects
        fx_frame = ttk.LabelFrame(frm, text="Visual Effects")
        fx_frame.pack(fill=tk.X, padx=10, pady=6)
        self.zoom_on = tk.BooleanVar(value=True)
        self.zoom_val = tk.DoubleVar(value=1.05)
        self.vig_on = tk.BooleanVar(value=True)
        self.vig_val = tk.DoubleVar(value=0.3)
        self.speed_on = tk.BooleanVar(value=True)
        self.speed_val = tk.DoubleVar(value=5)
        self.noise_on = tk.BooleanVar(value=True)
        self.noise_val = tk.IntVar(value=12)

        row1 = ttk.Frame(fx_frame)
        row1.pack(fill=tk.X, padx=6, pady=2)
        ttk.Checkbutton(row1, text="Zoom", variable=self.zoom_on).pack(side=tk.LEFT, padx=4)
        ttk.Scale(row1, from_=1.01, to=1.30, variable=self.zoom_val, orient=tk.HORIZONTAL).pack(side=tk.LEFT, fill=tk.X, expand=True)

        row2 = ttk.Frame(fx_frame)
        row2.pack(fill=tk.X, padx=6, pady=2)
        ttk.Checkbutton(row2, text="Vignette", variable=self.vig_on).pack(side=tk.LEFT, padx=4)
        ttk.Scale(row2, from_=0.1, to=1.0, variable=self.vig_val, orient=tk.HORIZONTAL).pack(side=tk.LEFT, fill=tk.X, expand=True)

        row3 = ttk.Frame(fx_frame)
        row3.pack(fill=tk.X, padx=6, pady=2)
        ttk.Checkbutton(row3, text="Speed", variable=self.speed_on).pack(side=tk.LEFT, padx=4)
        ttk.Scale(row3, from_=0, to=20, variable=self.speed_val, orient=tk.HORIZONTAL).pack(side=tk.LEFT, fill=tk.X, expand=True)

        row4 = ttk.Frame(fx_frame)
        row4.pack(fill=tk.X, padx=6, pady=2)
        ttk.Checkbutton(row4, text="Grain", variable=self.noise_on).pack(side=tk.LEFT, padx=4)
        ttk.Scale(row4, from_=5, to=50, variable=self.noise_val, orient=tk.HORIZONTAL).pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Production
        prod_frame = ttk.LabelFrame(frm, text="Production Settings")
        prod_frame.pack(fill=tk.X, padx=10, pady=6)
        self.limit_qty = tk.IntVar(value=5)
        ttk.Label(prod_frame, text="Total Videos to Generate").pack(side=tk.LEFT, padx=6)
        ttk.Spinbox(prod_frame, from_=1, to=5000, textvariable=self.limit_qty, width=8).pack(side=tk.LEFT)

    def _build_meta_tab(self):
        frm = self.tab_meta
        self.spoof_on = tk.BooleanVar(value=True)

        top = ttk.Frame(frm)
        top.pack(fill=tk.X, padx=10, pady=6)
        ttk.Checkbutton(top, text="Enable Metadata Spoofing", variable=self.spoof_on).pack(side=tk.LEFT, padx=6)

        device_frame = ttk.LabelFrame(frm, text="Device Signature")
        device_frame.pack(fill=tk.X, padx=10, pady=6)
        device_presets = ["🎲 Random Mobile (Recommended)", "🚫 Clean / No Metadata"]
        device_presets += [f"{hp['make']} {hp['model']}" for hp in MOBILE_POOL_DATA]
        self.device_preset = tk.StringVar(value=device_presets[0])
        ttk.Combobox(device_frame, textvariable=self.device_preset, values=device_presets, state="readonly", width=50).pack(side=tk.LEFT, padx=6)

        editor_frame = ttk.LabelFrame(frm, text="Editor Signature")
        editor_frame.pack(fill=tk.X, padx=10, pady=6)
        editor_options = ["🎲 Random Editor (Recommended)"] + EDITOR_POOL
        self.editor_choice = tk.StringVar(value=editor_options[0])
        ttk.Combobox(editor_frame, textvariable=self.editor_choice, values=editor_options, state="readonly", width=50).pack(side=tk.LEFT, padx=6)

        geo_frame = ttk.LabelFrame(frm, text="Geo Location")
        geo_frame.pack(fill=tk.X, padx=10, pady=6)
        self.geo_mode = tk.StringVar(value="None (Off)")
        ttk.Combobox(geo_frame, textvariable=self.geo_mode,
                     values=["None (Off)", "Random Global", "Specific Target"], state="readonly", width=20,
                     ).pack(side=tk.LEFT, padx=6)
        self.target_lat = tk.DoubleVar(value=40.7128)
        self.target_long = tk.DoubleVar(value=-74.0060)
        ttk.Label(geo_frame, text="Lat").pack(side=tk.LEFT, padx=4)
        ttk.Spinbox(geo_frame, from_=-90.0, to=90.0, increment=0.0001, textvariable=self.target_lat, width=10).pack(side=tk.LEFT)
        ttk.Label(geo_frame, text="Long").pack(side=tk.LEFT, padx=4)
        ttk.Spinbox(geo_frame, from_=-180.0, to=180.0, increment=0.0001, textvariable=self.target_long, width=10).pack(side=tk.LEFT)

        author_frame = ttk.LabelFrame(frm, text="Author")
        author_frame.pack(fill=tk.X, padx=10, pady=6)
        self.meta_author = tk.StringVar(value="Content Creator")
        ttk.Entry(author_frame, textvariable=self.meta_author, width=40).pack(side=tk.LEFT, padx=6)

    def _build_actions_tab(self):
        frm = self.tab_actions

        btns = ttk.Frame(frm)
        btns.pack(fill=tk.X, padx=10, pady=10)
        ttk.Button(btns, text="Preview (1 Video)", command=self._on_preview).pack(side=tk.LEFT, padx=6)
        ttk.Button(btns, text="Launch Production", command=self._on_launch).pack(side=tk.LEFT, padx=6)

        self.progress = ttk.Progressbar(frm, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress.pack(fill=tk.X, padx=10, pady=6)
        self.status_label = ttk.Label(frm, text="Idle")
        self.status_label.pack(fill=tk.X, padx=10)

        log_frame = ttk.LabelFrame(frm, text="Logs")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)
        self.log_text = tk.Text(log_frame, height=20, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    # ---------------- UI Helpers ----------------
    def _path_row(self, parent, label, var, is_dir=False):
        row = ttk.Frame(parent)
        row.pack(fill=tk.X, padx=10, pady=4)
        ttk.Label(row, text=label, width=22).pack(side=tk.LEFT)
        ttk.Entry(row, textvariable=var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)
        if is_dir:
            ttk.Button(row, text="Browse", command=lambda: self._pick_dir(var)).pack(side=tk.LEFT)
        else:
            ttk.Button(row, text="Browse", command=lambda: self._pick_file(var)).pack(side=tk.LEFT)

    def _pick_dir(self, var):
        path = filedialog.askdirectory()
        if path:
            var.set(path)

    def _pick_file(self, var):
        path = filedialog.askopenfilename(filetypes=[("Media", "*.mp4 *.mov *.mp3 *.wav"), ("All", "*.*")])
        if path:
            var.set(path)

    def _pick_color(self):
        color = colorchooser.askcolor(title="Pick color")
        if color and color[1]:
            self.t_color.set(color[1])

    def _toggle_mode(self):
        is_random = self.gen_mode.get() == "Random Mix (Single Folder)"
        self._set_widget_tree_state(self.random_frame, "normal" if is_random else "disabled")
        self._set_widget_tree_state(self.struct_frame, "normal" if not is_random else "disabled")
        if not is_random:
            self._toggle_struct_outro()

    def _toggle_vo(self):
        state = "normal" if self.enable_vo.get() else "disabled"
        for child in self._find_children_with_var(self.path_vo):
            child.configure(state=state)
        self._toggle_duration()

    def _toggle_music(self):
        state = "normal" if self.enable_music.get() else "disabled"
        for child in self._find_children_with_var(self.path_mus):
            child.configure(state=state)

    def _toggle_duration(self):
        if self.enable_vo.get():
            state = "disabled"
        else:
            state = "normal" if self.force_custom_dur.get() else "disabled"
        # Duration widgets are within assets tab; find by var
        for child in self._find_children_with_var(self.dur_min):
            child.configure(state=state)
        for child in self._find_children_with_var(self.dur_max):
            child.configure(state=state)

    def _toggle_struct_outro(self):
        is_enabled = self.use_struct_outro.get()
        state = "normal" if is_enabled else "disabled"
        self.struct_outro_entry.configure(state=state)
        self.struct_outro_btn.configure(state=state)

    def _find_children_with_var(self, var):
        # Helper to locate widgets linked to a Tk variable
        result = []
        for w in self.tab_assets.winfo_children():
            result.extend(self._walk_widgets(w))
        return [w for w in result if hasattr(w, 'cget') and 'textvariable' in w.keys() and w.cget('textvariable') == str(var)]

    def _walk_widgets(self, widget):
        all_w = [widget]
        for child in widget.winfo_children():
            all_w.extend(self._walk_widgets(child))
        return all_w

    def _set_widget_tree_state(self, widget, state):
        for child in widget.winfo_children():
            if "state" in child.keys():
                child.configure(state=state)
            self._set_widget_tree_state(child, state)

    def _log(self, msg):
        self.log_queue.put(msg)

    def _start_log_pump(self):
        def pump():
            try:
                while True:
                    msg = self.log_queue.get_nowait()
                    self.log_text.insert(tk.END, msg + "\n")
                    self.log_text.see(tk.END)
            except queue.Empty:
                pass
            try:
                while True:
                    fn = self.ui_queue.get_nowait()
                    fn()
            except queue.Empty:
                pass
            self.after(200, pump)
        self.after(200, pump)

    def _ui(self, fn):
        self.ui_queue.put(fn)

    def _set_progress(self, value):
        self.progress['value'] = value

    def _set_status(self, text):
        self.status_label.config(text=text)

    # ---------------- Actions ----------------
    def _collect_config(self, preview_mode=False):
        mode_random = (self.gen_mode.get() == "Random Mix (Single Folder)")

        if mode_random and not self.path_vid.get():
            messagebox.showerror("Error", "Video source folder required")
            return None
        if not mode_random and not all([self.path_hook.get(), self.path_prob.get(), self.path_sol.get(), self.path_cta.get()]):
            messagebox.showerror("Error", "Structured folders incomplete")
            return None
        if (not mode_random) and self.use_struct_outro.get() and not self.path_struct_outro.get():
            messagebox.showerror("Error", "Structured outro folder required")
            return None
        if self.enable_vo.get() and not self.path_vo.get():
            messagebox.showerror("Error", "Voice over folder required")
            return None
        if self.enable_music.get() and not self.path_mus.get():
            messagebox.showerror("Error", "Music folder required")
            return None
        if not self.path_out.get():
            messagebox.showerror("Error", "Output folder required")
            return None

        # duration mode
        if self.enable_vo.get():
            dur_mode = "vo_sync"
        else:
            dur_mode = "custom" if self.force_custom_dur.get() else "native"

        title_y = {"Top": "150", "Center": "(h-text_h)/2", "Bottom": "h-150"}.get(self.t_pos.get(), "(h-text_h)/2")

        # metadata
        if self.spoof_on.get():
            preset = self.device_preset.get()
            if "Random Mobile" in preset:
                preset_data = "random"
            elif "Clean" in preset:
                preset_data = "clean"
            else:
                preset_data = next((hp for hp in MOBILE_POOL_DATA if f"{hp['make']} {hp['model']}" == preset), "random")

            meta_config = {
                'on': True,
                'preset_data': preset_data,
                'geo_mode': self.geo_mode.get(),
                'lat': self.target_lat.get(),
                'long': self.target_long.get(),
                'author': self.meta_author.get(),
                'target_editor': self.editor_choice.get()
            }
        else:
            meta_config = {'on': False}

        cfg = {
            'path_vid': self.path_vid.get(),
            'path_vo': self.path_vo.get(),
            'path_mus': self.path_mus.get(),
            'path_out': self.path_out.get(),
            'path_hook': self.path_hook.get(),
            'path_prob': self.path_prob.get(),
            'path_sol': self.path_sol.get(),
            'path_cta': self.path_cta.get(),
            'path_struct_outro': self.path_struct_outro.get(),
            'file_intro': self.file_intro.get(),
            'file_outro': self.file_outro.get(),
            'mode_random': mode_random,
            'use_struct_outro': self.use_struct_outro.get(),
            'enable_vo': self.enable_vo.get(),
            'enable_music': self.enable_music.get(),
            'keep_ori_audio': self.keep_ori_audio.get(),
            'dur_mode': dur_mode,
            'dur_min': float(self.dur_min.get()),
            'dur_max': float(self.dur_max.get()),
            'min_clip': int(self.min_clip.get()),
            'max_clip': int(self.max_clip.get()),
            'use_intro': self.use_intro.get(),
            'use_outro': self.use_outro.get(),
            'use_ducking': self.use_ducking.get(),
            'use_title': self.use_title.get(),
            'title_text': self.title_text.get(),
            't_size': int(self.t_size.get()),
            't_color': self.t_color.get(),
            'title_y': title_y,
            'title_full_dur': self.title_full_dur.get(),
            'title_dur_sec': float(self.title_dur_sec.get()),
            'fx': {
                'speed': self.speed_on.get(),
                'speed_val': float(self.speed_val.get()),
                'zoom': self.zoom_on.get(),
                'zoom_val': float(self.zoom_val.get()),
                'vig': self.vig_on.get(),
                'vig_val': float(self.vig_val.get()),
                'noise': self.noise_on.get(),
                'noise_val': int(self.noise_val.get())
            },
            'hw_accel': self.hw_choice.get(),
            'bitrate_mode': self.bitrate_mode.get(),
            'meta': meta_config,
            'preview_mode': preview_mode
        }
        return cfg

    def _on_preview(self):
        cfg = self._collect_config(preview_mode=True)
        if not cfg:
            return

        ffmpeg_path = find_ffmpeg()
        if not ffmpeg_path:
            messagebox.showerror("Error", "FFmpeg not found. Install via Homebrew: brew install ffmpeg")
            return

        if cfg['enable_vo']:
            vos = get_files(cfg['path_vo'], ('.mp3', '.wav'))
            if not vos:
                messagebox.showerror("Error", "Folder VO kosong")
                return
            sample_vo = random.choice(vos)
        else:
            sample_vo = None

        if cfg['mode_random']:
            list_vid = get_files(cfg['path_vid'], ('.mp4', '.mov'))
            if not list_vid:
                messagebox.showerror("Error", "Video folder empty")
                return
            fixed_combo = None
        else:
            try:
                h = random.choice(get_files(cfg['path_hook'], ('.mp4', '.mov')))
                p = random.choice(get_files(cfg['path_prob'], ('.mp4', '.mov')))
                s = random.choice(get_files(cfg['path_sol'], ('.mp4', '.mov')))
                c = random.choice(get_files(cfg['path_cta'], ('.mp4', '.mov')))
                if cfg.get('use_struct_outro'):
                    fo = get_files(cfg['path_struct_outro'], ('.mp4', '.mov'))
                    if not fo:
                        messagebox.showerror("Error", "Structured outro folder empty")
                        return
                    o = random.choice(fo)
                    fixed_combo = (h, p, s, c, o)
                else:
                    fixed_combo = (h, p, s, c)
            except Exception:
                messagebox.showerror("Error", "Folder structure empty")
                return
            list_vid = []

        list_mus = get_files(cfg['path_mus'], ('.mp3', '.wav')) if cfg['enable_music'] else []

        self.status_label.config(text="Preview rendering...")
        self.progress['value'] = 0

        def worker():
            data_pack = (0, sample_vo, 1, cfg, {}, list_vid, list_mus, ffmpeg_path, fixed_combo)
            ok = process_single_video(data_pack, log_fn=self._log)
            self.log_queue.put("✅ Preview Ready" if ok else "❌ Preview Failed")
            self._ui(lambda: self._set_status("Idle"))
            self._ui(lambda: self._set_progress(100 if ok else 0))

        threading.Thread(target=worker, daemon=True).start()

    def _on_launch(self):
        cfg = self._collect_config(preview_mode=False)
        if not cfg:
            return

        save_config({
            'path_vid': cfg['path_vid'],
            'path_vo': cfg['path_vo'],
            'path_mus': cfg['path_mus'],
            'path_out': cfg['path_out'],
            'path_hook': cfg['path_hook'],
            'path_prob': cfg['path_prob'],
            'path_sol': cfg['path_sol'],
            'path_cta': cfg['path_cta'],
            'path_struct_outro': cfg['path_struct_outro'],
            'file_intro': cfg['file_intro'],
            'file_outro': cfg['file_outro']
        })

        ffmpeg_path = find_ffmpeg()
        if not ffmpeg_path:
            messagebox.showerror("Error", "FFmpeg not found. Install via Homebrew: brew install ffmpeg")
            return

        list_vo = get_files(cfg['path_vo'], ('.mp3', '.wav')) if cfg['enable_vo'] else []
        list_mus = get_files(cfg['path_mus'], ('.mp3', '.wav')) if cfg['enable_music'] else []
        list_vid, blueprints = [], []
        limit = int(self.limit_qty.get())

        if cfg['mode_random']:
            list_vid = get_files(cfg['path_vid'], ('.mp4', '.mov'))
            if not list_vid:
                messagebox.showerror("Error", "Video folder empty")
                return

            min_k = int(self.min_clip.get())
            max_k = int(self.max_clip.get())
            n = len(list_vid)

            max_unique = 0
            for k in range(min_k, max_k + 1):
                if n >= k:
                    max_unique += perm_count(n, k)
                else:
                    max_unique += n ** k

            unique_target = min(limit, max_unique)
            if limit > max_unique:
                self._log("⚠️ Unik kombinasi sudah habis. Output dibatasi ke jumlah unik.")

            signatures = set()
            attempts = 0
            max_attempts = max(100, unique_target * 50)

            while len(blueprints) < unique_target and attempts < max_attempts:
                k = random.randint(min_k, max_k)
                if n >= k:
                    seq = tuple(random.sample(list_vid, k))
                else:
                    seq = tuple(random.choices(list_vid, k=k))
                if seq not in signatures:
                    signatures.add(seq)
                    blueprints.append(seq)
                    attempts = 0
                else:
                    attempts += 1

            if len(blueprints) < unique_target:
                self._log("⚠️ Kesulitan mencapai semua kombinasi unik. Output dibatasi.")
        else:
            fh = get_files(cfg['path_hook'], ('.mp4', '.mov'))
            fp = get_files(cfg['path_prob'], ('.mp4', '.mov'))
            fs = get_files(cfg['path_sol'], ('.mp4', '.mov'))
            fc = get_files(cfg['path_cta'], ('.mp4', '.mov'))
            if not (fh and fp and fs and fc):
                messagebox.showerror("Error", "Structured folders incomplete")
                return
            if cfg.get('use_struct_outro'):
                fo = get_files(cfg['path_struct_outro'], ('.mp4', '.mov'))
                if not fo:
                    messagebox.showerror("Error", "Structured outro folder empty")
                    return
                blueprints, max_possibilities = generate_structured_blueprints(fh, fp, fs, fc, fo, limit)
            else:
                blueprints, max_possibilities = generate_smart_blueprints(fh, fp, fs, fc, limit)
            self._log(f"📊 Found {len(blueprints)} UNIQUE combinations.")
            if limit > max_possibilities:
                self._log("⚠️ Unik kombinasi sudah habis. Output dibatasi ke jumlah unik.")

        final_limit = len(blueprints)
        if final_limit == 0:
            messagebox.showerror("Error", "No valid combinations to render")
            return

        if cfg['enable_vo']:
            pool_vo = list_vo.copy()
            random.shuffle(pool_vo)
            while len(pool_vo) < final_limit:
                pool_vo.extend(list_vo.copy())
            loop_vo = pool_vo[:final_limit]
        else:
            loop_vo = [None] * final_limit

        jobs_data = []
        for i in range(final_limit):
            jobs_data.append((i, loop_vo[i], final_limit, cfg, {}, list_vid, list_mus, ffmpeg_path, blueprints[i]))

        self.status_label.config(text=f"Rendering {final_limit} videos...")
        self.progress['value'] = 0

        def worker():
            completed = 0
            with concurrent.futures.ThreadPoolExecutor(max_workers=int(self.threads_val.get())) as executor:
                futures = [executor.submit(process_single_video, d, self._log) for d in jobs_data]
                for future in concurrent.futures.as_completed(futures):
                    if future.result():
                        completed += 1
                    prog = int((completed / final_limit) * 100)
                    self._ui(lambda p=prog: self._set_progress(p))
                    self._ui(lambda c=completed, t=final_limit: self._set_status(f"Completed: {c}/{t}"))
            self._log(f"🎉 RENDER SELESAI! {completed} Video berhasil dibuat.")

        threading.Thread(target=worker, daemon=True).start()

    def _apply_saved_config(self):
        cfg = self.saved_config
        if not cfg:
            return
        self.path_vid.set(cfg.get('path_vid', ''))
        self.path_vo.set(cfg.get('path_vo', ''))
        self.path_mus.set(cfg.get('path_mus', ''))
        self.path_out.set(cfg.get('path_out', ''))
        self.path_hook.set(cfg.get('path_hook', ''))
        self.path_prob.set(cfg.get('path_prob', ''))
        self.path_sol.set(cfg.get('path_sol', ''))
        self.path_cta.set(cfg.get('path_cta', ''))
        self.path_struct_outro.set(cfg.get('path_struct_outro', ''))
        self.file_intro.set(cfg.get('file_intro', ''))
        self.file_outro.set(cfg.get('file_outro', ''))


if __name__ == "__main__":
    app = App()
    app.mainloop()
