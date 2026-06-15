#!/usr/bin/env python3
"""
Local Video Downloader - Runs on your PC
Supports YouTube, M3U8/HLS streams, and Referer URLs
"""

import subprocess
import os
import re
from pathlib import Path
from datetime import datetime

# Try to import tkinter for GUI
try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog, scrolledtext
    import threading
    HAS_GUI = True
except ImportError:
    HAS_GUI = False
    print("Tkinter not available. Using command line mode.")

if HAS_GUI:
    import yt_dlp

    class LocalVideoDownloader:
        def __init__(self, root):
            self.root = root
            self.root.title("Video Downloader - Local PC (YouTube + M3U8)")
            self.root.geometry("850x700")
            self.root.resizable(True, True)
            self.setup_ui()
            self.check_dependencies()
        
        def setup_ui(self):
            main_frame = ttk.Frame(self.root, padding="20")
            main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Title
            title = ttk.Label(main_frame, text="🎥 Video Downloader (Local PC)", font=('Arial', 18, 'bold'))
            title.grid(row=0, column=0, columnspan=3, pady=(0, 10))
            
            subtitle = ttk.Label(main_frame, text="YouTube | M3U8/HLS Streams | Referer Support", font=('Arial', 10))
            subtitle.grid(row=1, column=0, columnspan=3, pady=(0, 20))
            
            # URL Input
            ttk.Label(main_frame, text="Video/M3U8 URL:", font=('Arial', 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
            self.url_entry = ttk.Entry(main_frame, width=60, font=('Arial', 10))
            self.url_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
            
            paste_btn = ttk.Button(main_frame, text="📋 Paste", command=self.paste_url)
            paste_btn.grid(row=2, column=2, padx=(5, 0))
            
            # Referer URL (for M3U8)
            ttk.Label(main_frame, text="Referer URL (for M3U8):", font=('Arial', 10)).grid(row=3, column=0, sticky=tk.W, pady=5)
            self.referer_entry = ttk.Entry(main_frame, width=60, font=('Arial', 10))
            self.referer_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
            
            ttk.Label(main_frame, text="(Required for protected M3U8 streams)", font=('Arial', 8)).grid(row=3, column=2, sticky=tk.W, padx=(5, 0))
            
            # Download Type
            ttk.Label(main_frame, text="Download Type:", font=('Arial', 10)).grid(row=4, column=0, sticky=tk.W, pady=5)
            self.download_type = tk.StringVar(value="auto")
            type_frame = ttk.Frame(main_frame)
            type_frame.grid(row=4, column=1, sticky=tk.W, pady=5, padx=(10, 0))
            ttk.Radiobutton(type_frame, text="Auto Detect", variable=self.download_type, value="auto").pack(side=tk.LEFT, padx=5)
            ttk.Radiobutton(type_frame, text="YouTube", variable=self.download_type, value="youtube").pack(side=tk.LEFT, padx=5)
            ttk.Radiobutton(type_frame, text="M3U8/HLS", variable=self.download_type, value="m3u8").pack(side=tk.LEFT, padx=5)
            
            # Save location
            ttk.Label(main_frame, text="Save to:", font=('Arial', 10)).grid(row=5, column=0, sticky=tk.W, pady=5)
            self.location_var = tk.StringVar(value=str(Path.home() / "Downloads"))
            location_entry = ttk.Entry(main_frame, textvariable=self.location_var, width=50)
            location_entry.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
            
            browse_btn = ttk.Button(main_frame, text="📁 Browse", command=self.browse_location)
            browse_btn.grid(row=5, column=2, padx=(5, 0))
            
            # Quality (for YouTube)
            ttk.Label(main_frame, text="Quality:", font=('Arial', 10)).grid(row=6, column=0, sticky=tk.W, pady=5)
            self.quality_var = tk.StringVar(value="best")
            quality_combo = ttk.Combobox(main_frame, textvariable=self.quality_var, 
                                          values=["best (Highest)", "1080p", "720p", "480p", "360p", "audio (MP3)"],
                                          width=30)
            quality_combo.grid(row=6, column=1, sticky=tk.W, pady=5, padx=(10, 0))
            
            # Progress bar
            self.progress = ttk.Progressbar(main_frame, mode='indeterminate', length=600)
            self.progress.grid(row=7, column=0, columnspan=3, pady=10)
            
            # Status text
            self.status_text = scrolledtext.ScrolledText(main_frame, height=12, width=80, wrap=tk.WORD)
            self.status_text.grid(row=8, column=0, columnspan=3, pady=10)
            
            # Download button
            self.download_btn = ttk.Button(main_frame, text="⬇️ DOWNLOAD VIDEO/STREAM", command=self.start_download)
            self.download_btn.grid(row=9, column=0, columnspan=3, pady=10)
            
            # Info text
            info_text = "💡 M3U8 streams need ffmpeg. Install with: sudo apt install ffmpeg"
            ttk.Label(main_frame, text=info_text, font=('Arial', 9), foreground='gray').grid(row=10, column=0, columnspan=3)
            
            # Configure grid
            self.root.columnconfigure(0, weight=1)
            main_frame.columnconfigure(1, weight=1)
        
        def check_dependencies(self):
            # Check ffmpeg for M3U8
            try:
                subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
                self.log_message("✅ ffmpeg found - M3U8 downloads available")
            except:
                self.log_message("⚠️ ffmpeg not found - M3U8 downloads will fail. Install: sudo apt install ffmpeg")
        
        def paste_url(self):
            try:
                url = self.root.clipboard_get()
                self.url_entry.delete(0, tk.END)
                self.url_entry.insert(0, url)
                self.log_message("📋 URL pasted")
            except:
                self.log_message("❌ Could not paste")
        
        def browse_location(self):
            directory = filedialog.askdirectory(initialdir=self.location_var.get())
            if directory:
                self.location_var.set(directory)
                self.log_message(f"📁 Save location: {directory}")
        
        def log_message(self, message):
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
            self.status_text.see(tk.END)
            self.root.update()
        
        def start_download(self):
            url = self.url_entry.get().strip()
            if not url:
                messagebox.showerror("Error", "Please enter a URL")
                return
            
            # Auto-detect download type
            download_type = self.download_type.get()
            if download_type == "auto":
                if '.m3u8' in url.lower():
                    download_type = "m3u8"
                else:
                    download_type = "youtube"
            
            self.download_btn.config(state='disabled')
            self.progress.start()
            
            thread = threading.Thread(target=self.download_video, args=(url, download_type))
            thread.start()
        
        def download_video(self, url, download_type):
            try:
                if download_type == "m3u8":
                    self.download_m3u8(url)
                else:
                    self.download_youtube(url)
            except Exception as e:
                self.log_message(f"❌ Error: {e}")
            finally:
                self.progress.stop()
                self.root.after(0, lambda: self.download_btn.config(state='normal'))
        
        def download_m3u8(self, url):
            """Download M3U8/HLS stream with ffmpeg"""
            referer = self.referer_entry.get().strip()
            save_path = self.location_var.get()
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(save_path, f"m3u8_video_{timestamp}.mp4")
            
            self.log_message(f"🎬 Downloading M3U8 stream...")
            self.log_message(f"📋 URL: {url}")
            if referer:
                self.log_message(f"🔗 Referer: {referer}")
            self.log_message(f"💾 Save to: {output_file}")
            
            # Build ffmpeg command
            cmd = ['ffmpeg', '-y']
            if referer:
                cmd.extend(['-headers', f'Referer: {referer}\r\n'])
            cmd.extend(['-user_agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'])
            cmd.extend(['-i', url, '-c', 'copy', '-bsf:a', 'aac_adtstoasc', output_file])
            
            # Run ffmpeg
            process = subprocess.run(cmd, capture_output=True, text=True)
            
            if process.returncode == 0 and os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                size = os.path.getsize(output_file) / (1024 * 1024)
                self.log_message(f"\n✅ Download complete!")
                self.log_message(f"📄 File: {os.path.basename(output_file)}")
                self.log_message(f"💾 Size: {size:.2f} MB")
                self.log_message(f"📍 Location: {output_file}")
                
                # Ask to open folder
                if messagebox.askyesno("Success", f"Download complete!\n\nOpen folder?"):
                    subprocess.run(['xdg-open', save_path])
            else:
                error_msg = process.stderr if process.stderr else "Unknown error"
                self.log_message(f"❌ Download failed: {error_msg[:200]}")
                messagebox.showerror("Error", f"Download failed.\n\n{error_msg[:300]}")
        
        def download_youtube(self, url):
            """Download YouTube video using yt-dlp"""
            save_path = self.location_var.get()
            quality = self.quality_var.get()
            
            # Convert quality to yt-dlp format
            if quality == "best (Highest)":
                format_spec = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
            elif quality == "1080p":
                format_spec = "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]"
            elif quality == "720p":
                format_spec = "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]"
            elif quality == "480p":
                format_spec = "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]"
            elif quality == "360p":
                format_spec = "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360][ext=mp4]"
            elif quality == "audio (MP3)":
                format_spec = "bestaudio/best"
            else:
                format_spec = "best"
            
            self.log_message(f"🎬 Downloading YouTube video...")
            self.log_message(f"📋 URL: {url}")
            self.log_message(f"🎨 Quality: {quality}")
            
            ydl_opts = {
                'format': format_spec,
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
                'quiet': False,
            }
            
            if quality == "audio (MP3)":
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            self.log_message(f"✅ Download complete!")
            messagebox.showinfo("Success", "Download complete! Check your Downloads folder.")
        
        def progress_hook(self, d):
            if d['status'] == 'downloading':
                if '_percent_str' in d:
                    self.log_message(f"⬇️ {d['_percent_str']} at {d.get('_speed_str', 'unknown speed')}")
            elif d['status'] == 'finished':
                self.log_message(f"✅ Processing...")

    def main():
        root = tk.Tk()
        app = LocalVideoDownloader(root)
        root.mainloop()

else:
    def main():
        print("=" * 50)
        print("  🎥 Local Video Downloader (CLI Mode)")
        print("=" * 50)
        url = input("\n📋 Enter URL: ").strip()
        if url:
            if '.m3u8' in url.lower():
                referer = input("🔗 Referer URL (optional): ").strip()
                output = f"~/Downloads/m3u8_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
                cmd = f'ffmpeg -headers "Referer: {referer}" -i "{url}" -c copy -bsf:a aac_adtstoasc {output}'
                os.system(cmd)
            else:
                os.system(f'yt-dlp -o "~/Downloads/%(title)s.%(ext)s" "{url}"')

if __name__ == "__main__":
    main()
