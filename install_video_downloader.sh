#!/bin/bash
# One-command installer for Video Downloader

echo "Installing Video Downloader..."

# Download the Python script
curl -s -o ~/.local/bin/video-downloader https://raw.githubusercontent.com/mos238/myWebSite/main/local_downloader.py
chmod +x ~/.local/bin/video-downloader

# Create desktop entry
mkdir -p ~/.local/share/applications
cat > ~/.local/share/applications/video-downloader.desktop << 'DESKTOP'
[Desktop Entry]
Version=1.0
Type=Application
Name=Video Downloader
Comment=Download YouTube and M3U8 videos
Exec=python3 ~/.local/bin/video-downloader
Icon=video-x-generic
Terminal=false
Categories=AudioVideo;
DESKTOP

echo "✅ Installed! Run 'video-downloader' or find it in your apps menu"
