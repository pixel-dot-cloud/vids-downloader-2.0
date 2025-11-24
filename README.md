# VidsDL 2.1

<div align="center">

![VidsDL Logo](https://img.shields.io/badge/VidsDL-2.1-8b5cf6?style=for-the-badge)
[![License](https://img.shields.io/badge/License-Custom-blue?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey?style=for-the-badge)](https://github.com/pixel-dot-cloud/vids-downloader-2.0/releases)

**High-quality YouTube video & audio downloader with native desktop interface**

[Download for Windows](https://github.com/pixel-dot-cloud/vids-downloader-2.0/releases/download/windows/VidsDL-windows.exe) • [Download for Linux](#-linux) • [Features](#-features) • [Building](#-building-from-source)

</div>

---

> **Note:** This is VidsDL 2.1 - the continuation of the original VidsDL project, now with proper desktop releases for both Windows and Linux!

---

##  Features:

-  **High-Quality Downloads** - Up to 4K resolution
-  ** Shorts Detection** - Automatically changes quality for vertical videos
-  **Audio Extraction** - Download as MP3
-  **Multiple Formats** - MP4, WEBM, MOV, MP3
-  **Native Desktop App** - No browser required
-  **Modern Interface** - Clean, glassmorphism-styled UI

---

## 📥 Installation

### Windows

**Requirements:**
- Windows 10/11
- FFmpeg ([install guide](#installing-ffmpeg))

**Steps:**
1. Download `VidsDL.exe` from [Releases](https://github.com/pixel-dot-cloud/vids-downloader-2.0/releases)
2. Run `VidsDL.exe`
3. Done! 🎉

**Note:** First run may be slow (extracting resources). Windows Defender might show a warning - this is a false positive from PyInstaller packaging.

### 🐧 Linux

**Quick Install (Recommended):**
```bash
# Download source from releases
cd vids-downloader-2.0/linux
chmod +x install.sh
./install.sh
```

**What it does:**
- Installs Python dependencies
- Creates `vidsdl` command
- Adds app to application menu
- Sets up CLI tool

**Usage after install:**
```bash
# Launch GUI
vidsdl

# Or use CLI
vidsdl-cli https://youtube.com/watch?v=... --quality 1080
```

**Manual Installation:**
```bash
pip3 install flask flask-cors yt-dlp pywebview
python3 src/app.py
```
Then open: http://127.0.0.1:5000

---

## Usage

### GUI (Windows & Linux)

1. **Launch** the app
2. **Paste** YouTube URL
3. **Select** quality and format
4. **Download!**

Files save to:
- **Windows:** `downloads/` folder next to exe
- **Linux:** `~/Downloads/`

### CLI (Linux only)

```bash
# Basic usage
vidsdl-cli <URL>

# With options
vidsdl-cli https://youtube.com/watch?v=... --quality 1080 --format mp4

# Extract audio
vidsdl-cli https://youtube.com/watch?v=... --format mp3

# Options
  --quality, -q    Video quality (360|480|720|1080|1440|2160)
  --format, -f     Output format (mp4|webm|mov|mp3)
```

---

## 📋 Supported Formats

| Category | Formats |
|----------|---------|
| **Video** | MP4 (recommended), WEBM, MOV |
| **Audio** | MP3 |
| **Quality** | 360p, 480p, 720p, 1080p, 1440p, 4K |

** Tips:**
- MP4 recommended for best compatibility
- 1080p is the sweet spot for quality/size balance
- Shorts automatically download at maximum available quality

---

## Installing FFmpeg

FFmpeg is **required** for video processing.

### Windows:
```bash
# Using winget (recommended)
winget install FFmpeg

# Or download manually
```
Download from: https://ffmpeg.org/download.html

### Linux:
```bash
# Debian/Ubuntu/Kali
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch
sudo pacman -S ffmpeg
```

---

## Troubleshooting

### Windows

**Antivirus blocking exe?**
- Add exception for VidsDL.exe
- False positive from PyInstaller packaging

**Downloads failing?**
- Verify FFmpeg is installed: `ffmpeg -version`
- Some videos may have restrictions
- Try a different video

**App won't start?**
- Ensure Windows 10/11
- Check FFmpeg installation
- Run as administrator (if needed)

### Linux

**`vidsdl` command not found?**
```bash
source ~/.bashrc
# or
export PATH="$HOME/.local/bin:$PATH"
```

**Permission errors?**
```bash
sudo apt install ffmpeg python3-pip
pip3 install --break-system-packages flask flask-cors yt-dlp pywebview
```

**PyWebView issues?**
```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.1
```

---

## 🛠️ Building from Source

### Windows

**Requirements:**
- Python 3.8+
- PyInstaller

**Build:**
```bash
cd windows
build-single.bat
```

Output: `dist-release/VidsDL.exe`

### Linux

**Requirements:**
- Python 3.8+
- GTK3, WebKit2

**Install dependencies:**
```bash
sudo apt install python3-pip python3-gi gir1.2-webkit2-4.1 ffmpeg
pip3 install pyinstaller flask flask-cors yt-dlp pywebview
```

**Build:**
```bash
cd linux
chmod +x build-linux.sh
./build-linux.sh
```

Output: `dist/VidsDL-Linux`

---

##  File Locations

| Platform | Downloads | Temp Files |
|----------|-----------|------------|
| **Windows** | `downloads/` (next to exe) | Auto-cleaned |
| **Linux** | `~/Downloads/` | Auto-cleaned |

---

## ⚠️ Disclaimer

**This tool is for personal use only.**

Users are solely responsible for ensuring their use complies with:
- YouTube's Terms of Service
- Copyright laws
- Local regulations

The developers are NOT responsible for how users choose to use this tool.

**Use at your own risk.**

---

## 🙏 Credits

Built with:
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloader
- [PyWebView](https://pywebview.flowrl.com/) - Desktop UI
- [Flask](https://flask.palletsprojects.com/) - Backend server

---

## 📜 License

See [LICENSE](LICENSE) for details.

**TL;DR:** Personal use only, no commercial use, no redistribution of modified code.

---

## 🔄 Updates

Check [Releases](https://github.com/pixel-dot-cloud/vids-downloader-2.0/releases) for the latest version.

**Current:** v2.1.0

---

<div align="center">

**Made with 💜**

[Report Bug](https://github.com/pixel-dot-cloud/vids-downloader-2.0/issues) • [Request Feature](https://github.com/pixel-dot-cloud/vids-downloader-2.0/issues)

</div>
