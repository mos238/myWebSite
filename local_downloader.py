#!/usr/bin/env python3
"""
Local Video Downloader - Runs on your PC
Faster, more efficient, no server limitations
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
            self.root.title("Video Downloader - Local PC")
            self.root.geometry("800x600")
            self.root.resizable(True, True)
            self.setup_ui()
        
        def setup_ui(self):
            main_frame = ttk.Frame(self.root, padding="20")
            main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            title = ttk.Label(main_frame, text="🎥 Video Downloader (Local PC)", font=('Arial', 18, 'bold'))
            title.grid(row=0, column=0, columnspan=3, pady=(0, 20))
            
            ttk.Label(main_frame, text="Video URL:", font=('Arial', 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
            self.url_entry = ttk.Entry(main_frame, width=60, font=('Arial', 10))
            self.url_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
            
            paste_btn = ttk.Button(main_frame, text="📋 Paste", command=self.paste_url)
            paste_btn.grid(row=1, column=2, padx=(5, 0))
            
            ttk.Label(main_frame, text="Save to:", font=('Arial', 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
            self.location_var = tk.StringVar(value=str(Path.home() / "Downloads"))
            location_entry = ttk.Entry(main_frame, textvariable=self.location_var, width=50)
            location_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
            
            browse_btn = ttk.Button(main_frame, text="📁 Browse", command=self.browse_location)
            browse_btn.grid(row=2, column=2, padx=(5, 0))
            
            ttk.Label(main_frame, text="Quality:", font=('Arial', 10)).grid(row=3, column=0, sticky=tk.W, pady=5)
            self.quality_var = tk.StringVar(value="best")
            quality_combo = ttk.Combobox(main_frame, textvariable=self.quality_var, 
                                          values=["best (Highest)", "1080p", "720p", "480p", "360p", "audio (MP3)"],
                                          width=30)
            quality_combo.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
            
            self.download_btn = ttk.Button(main_frame, text="⬇️ DOWNLOAD VIDEO", command=self.start_download)
            self.download_btn.grid(row=4, column=0, columnspan=3, pady=20)
            
            self.status_text = scrolledtext.ScrolledText(main_frame, height=15, width=80, wrap=tk.WORD)
            self.status_text.grid(row=5, column=0, columnspan=3, pady=10)
            
            self.root.columnconfigure(0, weight=1)
            main_frame.columnconfigure(1, weight=1)
        
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
            
            self.download_btn.config(state='disabled')
            thread = threading.Thread(target=self.download_video, args=(url,))
            thread.start()
        
        def download_video(self, url):
            try:
                self.log_message(f"🎬 Downloading: {url}")
                save_path = self.location_var.get()
                
                ydl_opts = {
                    'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                    'progress_hooks': [self.progress_hook],
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                self.log_message("✅ Download complete!")
                self.root.after(0, lambda: self.download_btn.config(state='normal'))
            except Exception as e:
                self.log_message(f"❌ Error: {e}")
                self.root.after(0, lambda: self.download_btn.config(state='normal'))
        
        def progress_hook(self, d):
            if d['status'] == 'downloading':
                self.log_message(f"⬇️ Downloading... {d.get('_percent_str', '0%')}")
    
    def main():
        root = tk.Tk()
        app = LocalVideoDownloader(root)
        root.mainloop()

else:
    def main():
        print("=" * 50)
        print("  🎥 Local Video Downloader (CLI Mode)")
        print("=" * 50)
        url = input("\n📋 Enter video URL: ").strip()
        if url:
            os.system(f'yt-dlp -o "~/Downloads/%(title)s.%(ext)s" "{url}"')

if __name__ == "__main__":
    main()
