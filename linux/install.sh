#!/bin/bash
clear
echo "======================================"
echo "   VidsDL 2.1 - Quick Install"
echo "======================================"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install --break-system-packages flask flask-cors yt-dlp pywebview 2>/dev/null || pip3 install flask flask-cors yt-dlp pywebview

# Create local installation (no sudo needed!)
echo "📁 Installing VidsDL..."
INSTALL_DIR="$HOME/.local/share/VidsDL"
mkdir -p "$INSTALL_DIR"
cp app.py index.html "$INSTALL_DIR/"

# Create launcher command
mkdir -p "$HOME/.local/bin"
cat > "$HOME/.local/bin/vidsdl" << 'EOF'
#!/bin/bash
cd "$HOME/.local/share/VidsDL"
python3 app.py > /dev/null 2>&1 &
sleep 2
xdg-open http://127.0.0.1:5000 2>/dev/null
EOF
chmod +x "$HOME/.local/bin/vidsdl"

# Add to PATH if not already
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc 2>/dev/null
fi

# Create desktop entry (optional, no sudo)
mkdir -p "$HOME/.local/share/applications"
cat > "$HOME/.local/share/applications/vidsdl.desktop" << EOF
[Desktop Entry]
Type=Application
Name=VidsDL
Comment=YouTube Downloader
Exec=$HOME/.local/bin/vidsdl
Icon=video-x-generic
Categories=Network;AudioVideo;
Terminal=false
EOF

echo ""
echo "======================================"
echo "✅ Installation Complete!"
echo ""
echo "🚀 To run: vidsdl"
echo "   (or search 'VidsDL' in app menu)"
echo ""
echo "📁 Downloads save to: ~/Downloads"
echo ""
echo "⚠️  If 'vidsdl' command not found:"
echo "   Run: source ~/.bashrc"
echo "======================================"
