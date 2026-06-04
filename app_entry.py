import os
import sys
import subprocess
from pathlib import Path


def main() -> int:
    # Use a writable working directory for configs/output.
    app_data_dir = Path.home() / "Documents" / "NOCAPTION"
    app_data_dir.mkdir(parents=True, exist_ok=True)
    os.chdir(app_data_dir)

    # Resolve bundled script path (PyInstaller) or local path (dev).
    base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    script_path = base_dir / "NOCAPTION.py"

    if not script_path.exists():
        raise FileNotFoundError(f"Missing NOCAPTION.py at {script_path}")

    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(script_path),
        "--server.headless=false",
        "--browser.gatherUsageStats=false",
    ]

    # Launch Streamlit and let it open the browser.
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
