#!/bin/bash
# M3U8 Downloader - Complete Self-Contained Installer
# Download and run this file only - it contains everything!

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🚀 M3U8 Video Downloader Installer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "📦 Installing ffmpeg..."
    sudo apt update && sudo apt install ffmpeg -y
fi

# Create directories
mkdir -p "$HOME/.local/bin"

# Create the actual downloader script
cat > "$HOME/.local/bin/m3u8-downloader" << 'SCRIPT'
#!/bin/bash
# M3U8 Video Downloader

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

DOWNLOAD_DIR="$HOME/Downloads"
mkdir -p "$DOWNLOAD_DIR"

clear
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}              M3U8 VIDEO DOWNLOADER${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo ""

read -p "Enter M3U8 URL: " m3u8_url
[ -z "$m3u8_url" ] && echo -e "${RED}No URL entered${NC}" && exit 1

echo ""
read -p "Enter Referer URL (press Enter to skip): " referer_url

timestamp=$(date +"%Y%m%d_%H%M%S")
output_file="$DOWNLOAD_DIR/m3u8_video_${timestamp}.mp4"

echo ""
echo -e "${YELLOW}Downloading to: $output_file${NC}"
echo ""

ffmpeg -y \
    -headers "Referer: $referer_url" \
    -user_agent "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
    -i "$m3u8_url" \
    -c copy \
    -bsf:a aac_adtstoasc \
    "$output_file" 2>&1 | grep -E "time=|error" 

if [ -f "$output_file" ] && [ -s "$output_file" ]; then
    size=$(du -h "$output_file" | cut -f1)
    echo ""
    echo -e "${GREEN}✅ Download complete!${NC}"
    echo -e "📁 File: $output_file"
    echo -e "💾 Size: $size"
else
    echo -e "${RED}❌ Download failed${NC}"
fi
SCRIPT

chmod +x "$HOME/.local/bin/m3u8-downloader"

# Create desktop launcher
mkdir -p "$HOME/.local/share/applications"
cat > "$HOME/.local/share/applications/m3u8-downloader.desktop" << DESKTOP
[Desktop Entry]
Version=1.0
Type=Application
Name=M3U8 Video Downloader
Exec=$HOME/.local/bin/m3u8-downloader
Icon=utilities-terminal
Terminal=true
Categories=AudioVideo;
DESKTOP

# Update PATH
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    export PATH="$HOME/.local/bin:$PATH"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ INSTALLATION COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Run: m3u8-downloader"
echo ""
