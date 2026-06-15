#!/bin/bash

# Simple M3U8 Downloader
# Usage: ./m3u8_downloader.sh

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Download folder
DOWNLOAD_DIR="$HOME/Downloads"
mkdir -p "$DOWNLOAD_DIR"

# Function to download M3U8 video
download_m3u8() {
    local m3u8_url="$1"
    local referer_url="$2"
    
    # Create output filename
    local timestamp=$(date +"%Y%m%d_%H%M%S")
    local output_file="$DOWNLOAD_DIR/m3u8_video_${timestamp}.mp4"
    
    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}              Downloading M3U8 Video${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${CYAN}📹 M3U8 URL:${NC} $m3u8_url"
    echo -e "${CYAN}🔗 Referer:${NC} $referer_url"
    echo -e "${CYAN}💾 Save to:${NC} $output_file"
    echo ""
    echo -e "${YELLOW}Starting download...${NC}"
    echo ""
    
    # Build ffmpeg command with referer
    ffmpeg -y \
        -headers "Referer: $referer_url" \
        -user_agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
        -i "$m3u8_url" \
        -c copy \
        -bsf:a aac_adtstoasc \
        -movflags +faststart \
        "$output_file" 2>&1 | while IFS= read -r line; do
            # Show progress
            if [[ "$line" =~ time=([0-9:]+) ]]; then
                echo -ne "\r${GREEN}Progress: ${BASH_REMATCH[1]}${NC}    "
            fi
        done
    
    echo "" # New line after progress
    
    # Check if download was successful
    if [ -f "$output_file" ] && [ -s "$output_file" ]; then
        local file_size=$(du -h "$output_file" | cut -f1)
        echo ""
        echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}✅ DOWNLOAD COMPLETE!${NC}"
        echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
        echo ""
        echo -e "${CYAN}📹 File:${NC} $(basename "$output_file")"
        echo -e "${CYAN}💾 Size:${NC} $file_size"
        echo -e "${CYAN}📁 Location:${NC} $DOWNLOAD_DIR"
        echo ""
        return 0
    else
        echo ""
        echo -e "${RED}════════════════════════════════════════════════════════${NC}"
        echo -e "${RED}❌ DOWNLOAD FAILED!${NC}"
        echo -e "${RED}════════════════════════════════════════════════════════${NC}"
        echo ""
        echo -e "${YELLOW}Possible reasons:${NC}"
        echo "  • M3U8 link expired (get a fresh link)"
        echo "  • Wrong referer URL"
        echo "  • Network connection issue"
        echo ""
        return 1
    fi
}

# Main script
clear
echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${GREEN}              SIMPLE M3U8 DOWNLOADER                       ${BLUE}║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}This script downloads M3U8 videos using ffmpeg${NC}"
echo -e "${YELLOW}Make sure you have ffmpeg installed: sudo apt-get install ffmpeg${NC}"
echo ""

# Get M3U8 URL
echo -n -e "${GREEN}➤ Enter M3U8 URL: ${NC}"
read -r m3u8_url

if [ -z "$m3u8_url" ]; then
    echo -e "${RED}No URL entered! Exiting...${NC}"
    exit 1
fi

echo ""

# Get Referer URL
echo -e "${CYAN}💡 The referer is the website where the video is from${NC}"
echo -e "${CYAN}   Example: https://example.com/video-page${NC}"
echo ""
echo -n -e "${GREEN}➤ Enter Referer URL: ${NC}"
read -r referer_url

if [ -z "$referer_url" ]; then
    echo -e "${YELLOW}⚠ No referer provided. Continuing anyway...${NC}"
fi

# Download the video
download_m3u8 "$m3u8_url" "$referer_url"

# Ask to play
if [ $? -eq 0 ]; then
    echo ""
    echo -n -e "${YELLOW}🎬 Play video now? (y/n): ${NC}"
    read -r play_choice
    if [[ "$play_choice" =~ ^[Yy]$ ]]; then
        if command -v vlc &> /dev/null; then
            vlc "$DOWNLOAD_DIR/m3u8_video_"* 2>/dev/null &
        elif command -v mpv &> /dev/null; then
            mpv "$DOWNLOAD_DIR/m3u8_video_"* 2>/dev/null &
        else
            echo -e "${YELLOW}No player found. File saved in: $DOWNLOAD_DIR${NC}"
        fi
    fi
fi

echo ""
echo -e "${GREEN}Done!${NC}"
