# VidsDL 2.0

High-quality YouTube video & audio downloader with native desktop interface.

> **Note:** This is VidsDL 2.0 - the continuation of the original VidsDL project, now with a proper desktop release!

---

## 📥 Download

Grab the latest release from the [Releases](../../releases) page.

---

## ✨ Features

- 🎬 Download YouTube videos in multiple qualities (360p to 4K)
- 🎵 Extract audio as MP3
- 📦 Multiple format support: MP4, WEBM, MOV, MP3
- 🖥️ Native desktop app (no browser required)
- ⚡ Fast downloads with quality selection
- 🎨 Clean, modern interface

---

## 🚀 Quick Start

1. **Download** `VidsDL.exe` from releases
2. **Install FFmpeg** (required):
   ```bash
   winget install FFmpeg
   ```
   Or download from: https://ffmpeg.org/download.html
3. **Run** `VidsDL.exe`
4. **Paste** a YouTube URL
5. **Select** quality and format
6. **Download!** Files save to `downloads/` folder

---

## 📋 Requirements

- Windows 10/11
- FFmpeg (for video processing)

---

## 🎯 Supported Formats

**Video:**
- MP4 (recommended)
- WEBM
- MOV

**Audio:**
- MP3

**Quality:**
- 360p, 480p, 720p, 1080p, 1440p, 4K

---

## 🐛 Troubleshooting

**Downloads fail or stuck at low quality?**
- Make sure FFmpeg is installed and in PATH
- Some videos may have quality restrictions
- Try a different video to test

**Antivirus blocking the exe?**
- This is a false positive (common with PyInstaller)
- Add exception or use Windows Defender

**App won't start?**
- Make sure you have Windows 10/11
- Check if FFmpeg is installed

---

## 📁 File Locations

- **Downloads:** `downloads/` folder (created next to VidsDL.exe)
- **Temporary files:** Automatically cleaned after download

---

## 🔄 Updates

To get the latest version, download the newest release from the releases page.

---

## 💡 Tips

- For best compatibility, use MP4 format
- 1080p is the sweet spot for quality/size
- MP3 downloads extract audio only (smaller file size)

---

## ⚠️ Disclaimer

This tool is for personal use only. Respect copyright laws and YouTube's Terms of Service.

---

## 🙏 Credits

Built with:
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloader
- [PyWebView](https://pywebview.flowrl.com/) - Desktop UI
- [Flask](https://flask.palletsprojects.com/) - Backend server

---

**Made with 💜**
