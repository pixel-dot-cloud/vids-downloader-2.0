# VidsDL 2.1 - Linux Installation

## Quick Install (One Command!)

```bash
chmod +x install.sh && ./install.sh
```

That's it! 🎉

---

## What it does:

- ✅ Installs Python dependencies
- ✅ Sets up VidsDL in your home folder
- ✅ Creates `vidsdl` command
- ✅ Adds app to your menu

---

## Usage:

```bash
# Launch GUI
vidsdl

# Or search "VidsDL" in your app menu
```

---

## Requirements:

- Python 3.8+
- FFmpeg: `sudo apt install ffmpeg`

---

## Manual Installation:

If the script doesn't work:

```bash
# 1. Install dependencies
pip3 install flask flask-cors yt-dlp pywebview

# 2. Run directly
python3 app.py
```

Then open: http://127.0.0.1:5000

---

## Uninstall:

```bash
rm -rf ~/.local/share/VidsDL
rm ~/.local/bin/vidsdl
rm ~/.local/share/applications/vidsdl.desktop
```

---

**Downloads save to:** `~/Downloads/`
