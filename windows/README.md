# 🖥️ NOCAPTION V4 — Panduan Build Windows

## 📦 Apa yang ada di folder ini?

| File | Fungsi |
|---|---|
| `nocaption_win.py` | Source code utama (sudah kompatibel Windows) |
| `requirements.txt` | Daftar dependency Python |
| `NOCAPTION_WIN.spec` | Konfigurasi PyInstaller |
| `build.bat` | Script build 1-klik |
| `download_ffmpeg.ps1` | Script download FFmpeg otomatis |
| `installer.iss` | Script Inno Setup (buat installer `.exe`) |

---

## 🚀 Cara Build (di komputer Windows)

### Opsi A: Build Manual di Komputer Windows

#### Prasyarat
1. **Python 3.10+** — Download dari https://www.python.org/downloads/
   - ⚠️ Saat install, **CENTANG** "Add Python to PATH"
2. **FFmpeg** — Akan di-download otomatis oleh script

#### Langkah-langkah

```
1. Copy seluruh folder "windows" ke komputer Windows

2. Buka Command Prompt / PowerShell di folder tersebut

3. Download FFmpeg (jalankan di PowerShell):
   powershell -ExecutionPolicy Bypass -File download_ffmpeg.ps1

4. Jalankan build:
   build.bat

5. Hasil build ada di folder:
   dist\NOCAPTION V4\NOCAPTION V4.exe
```

#### Membuat Installer (Opsional)
1. Install **Inno Setup 6** dari https://jrsoftware.org/isdl.php
2. Buka `installer.iss` dengan Inno Setup
3. Klik **Build > Compile**
4. Installer akan muncul di `installer_output\NOCAPTION_V4_Setup.exe`

---

### Opsi B: Build Otomatis via GitHub Actions (TANPA komputer Windows)

1. Buat repository GitHub baru
2. Upload seluruh folder `nocaption_app` ke repository
3. Pastikan struktur folder seperti ini:
   ```
   repository/
   ├── nocaption_app/
   │   ├── windows/
   │   │   ├── nocaption_win.py
   │   │   ├── requirements.txt
   │   │   ├── NOCAPTION_WIN.spec
   │   │   ├── download_ffmpeg.ps1
   │   │   └── ...
   │   └── .github/
   │       └── workflows/
   │           └── build-windows.yml
   ```
4. Push ke branch `main`
5. Buka tab **Actions** di GitHub
6. Workflow "Build NOCAPTION V4 Windows" akan berjalan otomatis
7. Download file ZIP hasil build dari **Artifacts**

---

## 📤 Cara Share ke Pengguna Windows

### Opsi 1: Portable ZIP (Tanpa Install)
1. Setelah build selesai, ZIP seluruh folder `dist\NOCAPTION V4\`
2. Share file ZIP tersebut
3. Pengguna cukup extract dan double-click `NOCAPTION V4.exe`

### Opsi 2: Installer EXE (Profesional)
1. Build installer menggunakan Inno Setup (lihat langkah di atas)
2. Share file `NOCAPTION_V4_Setup.exe`
3. Pengguna double-click installer, ikuti wizard, selesai!

---

## ⚙️ Catatan Teknis

### FFmpeg
- FFmpeg sudah di-bundle di dalam build, jadi pengguna **TIDAK perlu install FFmpeg** terpisah
- Jika FFmpeg tidak ter-bundle, aplikasi akan cari di PATH dan lokasi umum Windows

### Hardware Acceleration
- **CPU (libx264)** — Default, paling stabil, semua komputer support
- **NVIDIA GPU (nvenc)** — Butuh GPU NVIDIA + driver terbaru
- **Intel QSV** — Butuh GPU Intel terintegrasi
- **AMD AMF** — Butuh GPU AMD

### Icon
- Taruh file `icon.ico` di folder `windows/` sebelum build untuk custom icon
- Jika tidak ada, build tetap berjalan tanpa icon

---

## 🔧 Troubleshooting

| Masalah | Solusi |
|---|---|
| `Python not found` | Install Python, pastikan centang "Add to PATH" |
| `FFmpeg not found` | Jalankan `download_ffmpeg.ps1` dulu |
| `ModuleNotFoundError` | Jalankan `pip install -r requirements.txt` |
| Antivirus blokir .exe | Tambahkan exception di antivirus |
| App tidak mau buka | Coba jalankan dari Command Prompt untuk lihat error |
