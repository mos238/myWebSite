#!/bin/bash

# Standalone script to create desktop launcher for M3U8 Downloader

echo "Creating desktop launcher for M3U8 Downloader..."

# Get the actual script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create desktop entry
cat > "$HOME/.local/share/applications/m3u8-downloader.desktop" << DESKTOP
[Desktop Entry]
Version=1.0
Type=Application
Name=M3U8 Video Downloader
Comment=Download M3U8/HLS video streams
Exec=$SCRIPT_DIR/m3u8_downloader.sh
Icon=utilities-terminal
Terminal=true
Categories=AudioVideo;Network;
Keywords=video;downloader;m3u8;hls;
StartupNotify=true
DESKTOP

# Also create on desktop
cp "$HOME/.local/share/applications/m3u8-downloader.desktop" "$HOME/Desktop/" 2>/dev/null
chmod +x "$HOME/Desktop/m3u8-downloader.desktop" 2>/dev/null

# Update database
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null

echo ""
echo "✅ Desktop launcher created!"
echo ""
echo "You can now find 'M3U8 Video Downloader' in your applications menu"
echo "or double-click the icon on your desktop (if created)"
echo ""
DESKTOP

chmod +x create_desktop_launcher.sh

# Update tools.html to include the desktop launcher info
cat > update_tools_launcher.sh << 'EOF'
#!/bin/bash

# Update tools.html with desktop launcher info
cd /home/zeus/Documents/projects/CodecademyExamPrep/myWebSite

# Add desktop launcher tool card
sed -i '/One-Click Installer/,/Download Installer/ {
    a\
            </div>\
            <div class="tool-card">\
                <div class="tool-icon">🖥️</div>\
                <div class="tool-title">Desktop Launcher Creator</div>\
                <div class="tool-description">Creates a desktop shortcut and adds to Ubuntu applications menu. One-click launch after install.</div>\
                <div class="tool-downloads">\
                    <a href="create_desktop_launcher.sh" download class="download-btn">Download Launcher Script</a>\
                </div>
}' tools.html

echo "Tools page updated with desktop launcher"
