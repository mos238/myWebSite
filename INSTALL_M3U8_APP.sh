#!/bin/bash
# One-click installer for M3U8 Video Downloader App

echo "Installing M3U8 Video Downloader..."

# Download files
wget https://raw.githubusercontent.com/mos238/myWebSite/main/m3u8_gui.py
wget https://raw.githubusercontent.com/mos238/myWebSite/main/launch_m3u8.sh
wget https://raw.githubusercontent.com/mos238/myWebSite/main/m3u8-downloader.desktop

# Make executable
chmod +x m3u8_gui.py launch_m3u8.sh

# Install
cp m3u8-downloader.desktop ~/.local/share/applications/

echo "✅ Installation complete!"
echo "Find 'M3U8 Video Downloader' in your apps menu"
