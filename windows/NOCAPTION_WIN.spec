# -*- mode: python ; coding: utf-8 -*-
# NOCAPTION_WIN.spec
# PyInstaller spec file for NOCAPTION V4 (Windows build)
# Usage: pyinstaller NOCAPTION_WIN.spec

import os

spec_dir = os.path.dirname(os.path.abspath(SPEC))

# ── Icon (optional – build succeeds without it) ─────────────────────────────
icon_path = os.path.join(spec_dir, 'icon.ico')
app_icon = icon_path if os.path.isfile(icon_path) else None

# ── FFmpeg binaries to bundle ────────────────────────────────────────────────
ffmpeg_binaries = []
for exe_name in ('ffmpeg.exe', 'ffprobe.exe'):
    exe_path = os.path.join(spec_dir, exe_name)
    if os.path.isfile(exe_path):
        # (source, dest_folder_inside_bundle)
        ffmpeg_binaries.append((exe_path, '.'))

# ── Analysis ─────────────────────────────────────────────────────────────────
a = Analysis(
    [os.path.join(spec_dir, 'nocaption_win.py')],
    pathex=[spec_dir],
    binaries=ffmpeg_binaries,
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

# ── PYZ (bytecode archive) ──────────────────────────────────────────────────
pyz = PYZ(a.pure)

# ── EXE ──────────────────────────────────────────────────────────────────────
exe = EXE(
    pyz,
    a.scripts,
    [],                       # empty → one-folder mode (collected in COLLECT)
    exclude_binaries=True,    # binaries go into COLLECT, not EXE
    name='NOCAPTION V4',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,            # windowed mode – no terminal window
    disable_windowed_traceback=False,
    icon=app_icon,
)

# ── COLLECT (one-folder bundle) ──────────────────────────────────────────────
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='NOCAPTION V4',
)
