#!/bin/bash

# Update tools.html with the simple M3U8 downloader
sed -i '/M3U8 Downloader (Linux)/,/Download Bash Script/ {
    s|m3u8-dl.sh|m3u8_downloader.sh|g
    s|Download Bash Script|Download Simple Script|g
}' tools.html

# Also add the installer
sed -i '/<!-- M3U8 GUI App - Ubuntu -->/i\
            <!-- One-Click Installer -->\
            <div class="tool-card">\
                <div class="tool-icon">🚀</div>\
                <div class="tool-title">One-Click Installer</div>\
                <div class="tool-description">Automatically installs the M3U8 downloader with desktop shortcut. Works on Ubuntu/Debian.</div>\
                <div class="tool-downloads">\
                    <a href="install_m3u8_app.sh" download class="download-btn">Download Installer</a>\
                </div>\
            </div>' tools.html

echo "Tools page updated"
