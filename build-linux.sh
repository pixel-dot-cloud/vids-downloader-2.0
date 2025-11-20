#!/bin/bash
echo "========================================"
echo "   VidsDL v2.1 - Linux Build"
echo "========================================"
echo ""

# Check if icon exists
if [ ! -f "icon.png" ]; then
    echo "WARNING: icon.png not found (optional)"
fi

echo "Building single executable for Linux..."
echo "This may take 5-10 minutes..."
echo ""

# Build single file
pyinstaller --noconfirm \
    --onefile \
    --windowed \
    --name "VidsDL-Linux" \
    --add-data "index.html:." \
    --collect-all yt_dlp \
    app.py

echo ""
echo "========================================"
echo "Build Complete!"
echo ""
echo "Location: dist/VidsDL-Linux"
echo "Size: ~30-40 MB"
echo ""
echo "To run: ./dist/VidsDL-Linux"
echo "========================================"
echo ""
