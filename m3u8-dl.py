#!/usr/bin/env python3
"""
M3U8 Video Downloader - Cross Platform
Works on Windows, Mac, Linux
"""

import subprocess
import sys
import os
from datetime import datetime

def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except:
        return False

def install_instructions():
    print("\n❌ ffmpeg not installed!")
    print("\nInstallation:")
    print("  Linux:   sudo apt install ffmpeg")
    print("  Mac:     brew install ffmpeg")
    print("  Windows: https://ffmpeg.org/download.html")
    return False

def download():
    print("="*50)
    print("  🎥 M3U8 Video Downloader")
    print("="*50)
    
    if not check_ffmpeg():
        install_instructions()
        return
    
    url = input("\n📋 M3U8 URL: ").strip()
    if not url:
        print("❌ No URL provided")
        return
    
    filename = input("📝 Filename (press Enter for auto): ").strip()
    if not filename:
        filename = f"m3u8_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    elif not filename.endswith('.mp4'):
        filename += '.mp4'
    
    print(f"\n⬇️ Downloading to: {filename}")
    result = subprocess.run(['ffmpeg', '-i', url, '-c', 'copy', '-bsf:a', 'aac_adtstoasc', '-y', filename])
    
    if result.returncode == 0:
        size = os.path.getsize(filename) / (1024*1024)
        print(f"\n✅ Complete! Size: {size:.2f} MB")
    else:
        print("\n❌ Download failed")

if __name__ == "__main__":
    try:
        download()
    except KeyboardInterrupt:
        print("\n\n⚠️ Cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
