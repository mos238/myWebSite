#!/usr/bin/env python3

with open('index.html', 'r') as f:
    content = f.read()

# Find the Developer Tools section and restructure it
old_tools_section = '''                <div class="tools">
                    <h3>🛠️ Developer Tools</h3>
                    
                    <div class="tool-item">
                        <a href="https://mywebsite-m9qv.onrender.com" target="_blank" class="tool-link">
                            🎥 YouTube Downloader →
                        </a>
                        <div class="tool-description">Download videos in MP4 format</div>
                    </div>

                    <div class="tool-item">
                        <a href="dl_ytube.sh" download class="tool-link">
                            📜 Downloader Script →
                        </a>
                        <div class="tool-description">Bash script for terminal users</div>
                    </div>
                </div>'''

new_tools_section = '''                <div class="tools">
                    <h3>🛠️ Developer Tools</h3>
                    
                    <div class="tool-item">
                        <a href="https://mywebsite-m9qv.onrender.com" target="_blank" class="tool-link">
                            🎥 YouTube Downloader (Web App) →
                        </a>
                        <div class="tool-description">Download YouTube videos - Web interface</div>
                    </div>

                    <div class="tool-item">
                        <a href="dl_ytube.sh" download class="tool-link">
                            📜 YouTube Downloader Script →
                        </a>
                        <div class="tool-description">Bash script for terminal (YouTube)</div>
                    </div>

                    <div class="tool-item">
                        <a href="m3u8-dl.sh" download class="tool-link">
                            🐧 M3U8 Downloader (Linux) →
                        </a>
                        <div class="tool-description">Bash script for M3U8/HLS streams</div>
                    </div>

                    <div class="tool-item">
                        <a href="m3u8-dl.bat" download class="tool-link">
                            🪟 M3U8 Downloader (Windows) →
                        </a>
                        <div class="tool-description">Batch file for Windows users</div>
                    </div>

                    <div class="tool-item">
                        <a href="m3u8-dl.py" download class="tool-link">
                            🐍 M3U8 Downloader (Cross-platform) →
                        </a>
                        <div class="tool-description">Python script - works on any OS</div>
                    </div>

                    <div class="tool-item">
                        <a href="INSTALL_M3U8_APP.sh" download class="tool-link">
                            🖥️ M3U8 GUI App (Ubuntu) →
                        </a>
                        <div class="tool-description">Native desktop app - appears in "Show Apps"</div>
                    </div>

                    <div class="tool-item">
                        <a href="m3u8_gui.py" download class="tool-link">
                            🎨 M3U8 GUI App (Source) →
                        </a>
                        <div class="tool-description">Python GUI source code (with Referer support)</div>
                    </div>
                </div>'''

content = content.replace(old_tools_section, new_tools_section)

with open('index.html', 'w') as f:
    f.write(content)

print("✅ Developer Tools section reorganized!")
