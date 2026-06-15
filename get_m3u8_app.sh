#!/bin/bash
# Quick download - just gets the script, no installer

echo "Downloading M3U8 Downloader..."

# Create bin directory
mkdir -p "$HOME/.local/bin"

# Download the script directly from GitHub
curl -s -o "$HOME/.local/bin/m3u8-downloader" \
    "https://raw.githubusercontent.com/mos238/myWebSite/main/m3u8_downloader.sh"

chmod +x "$HOME/.local/bin/m3u8-downloader"

echo ""
echo "✅ Downloaded to ~/.local/bin/m3u8-downloader"
echo ""
echo "Run it with: m3u8-downloader"
echo ""
echo "Add to PATH? Run: echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
