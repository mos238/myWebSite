#!/usr/bin/env python3
"""
M3U8 Video Downloader - Native Ubuntu GUI App
Enhanced with better error handling and debugging
"""

import sys
import subprocess
import os
import re
from pathlib import Path
from datetime import datetime

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog, scrolledtext
    import threading
except ImportError:
    os.system('sudo apt update && sudo apt install python3-tk -y')
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog, scrolledtext
    import threading

class M3U8DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("M3U8 Video Downloader")
        self.root.geometry("750x650")
        self.root.resizable(True, True)
        
        self.setup_ui()
        self.check_ffmpeg()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title = ttk.Label(main_frame, text="🎥 M3U8 Video Downloader", 
                         font=('Arial', 18, 'bold'))
        title.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # M3U8 URL
        ttk.Label(main_frame, text="M3U8 URL:", font=('Arial', 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(main_frame, width=50, font=('Arial', 10))
        self.url_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        paste_btn = ttk.Button(main_frame, text="📋 Paste", command=self.paste_url)
        paste_btn.grid(row=1, column=2, padx=(5, 0))
        
        # Referer URL
        ttk.Label(main_frame, text="Referer URL:", font=('Arial', 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.referer_entry = ttk.Entry(main_frame, width=50, font=('Arial', 10))
        self.referer_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="(Required for some streams)", font=('Arial', 8)).grid(row=2, column=2, sticky=tk.W, padx=(5, 0))
        
        # User-Agent
        ttk.Label(main_frame, text="User-Agent:", font=('Arial', 10)).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.ua_entry = ttk.Entry(main_frame, width=50, font=('Arial', 10))
        self.ua_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        self.ua_entry.insert(0, "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36")
        
        # Filename
        ttk.Label(main_frame, text="Output Name:", font=('Arial', 10)).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.filename_entry = ttk.Entry(main_frame, width=50, font=('Arial', 10))
        self.filename_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        auto_btn = ttk.Button(main_frame, text="🎲 Auto", command=self.auto_name)
        auto_btn.grid(row=4, column=2, padx=(5, 0))
        
        # Save location
        ttk.Label(main_frame, text="Save Location:", font=('Arial', 10)).grid(row=5, column=0, sticky=tk.W, pady=5)
        self.location_var = tk.StringVar(value=str(Path.home() / "Videos"))
        location_entry = ttk.Entry(main_frame, textvariable=self.location_var, width=40)
        location_entry.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        browse_btn = ttk.Button(main_frame, text="📁 Browse", command=self.browse_location)
        browse_btn.grid(row=5, column=2, padx=(5, 0))
        
        # Progress
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate', length=400)
        self.progress.grid(row=6, column=0, columnspan=3, pady=20)
        
        # Status output
        self.status_text = scrolledtext.ScrolledText(main_frame, height=12, width=70, wrap=tk.WORD)
        self.status_text.grid(row=7, column=0, columnspan=3, pady=10)
        
        # Download button
        self.download_btn = ttk.Button(main_frame, text="⬇️ START DOWNLOAD", command=self.start_download)
        self.download_btn.grid(row=8, column=0, columnspan=3, pady=20)
        
        self.root.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
    
    def paste_url(self):
        try:
            url = self.root.clipboard_get()
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, url)
            self.log_message("📋 URL pasted from clipboard")
        except:
            self.log_message("❌ Could not paste from clipboard")
    
    def auto_name(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = f"m3u8_video_{timestamp}.mp4"
        self.filename_entry.delete(0, tk.END)
        self.filename_entry.insert(0, name)
        self.log_message(f"🎲 Auto-generated: {name}")
    
    def browse_location(self):
        directory = filedialog.askdirectory(initialdir=self.location_var.get())
        if directory:
            self.location_var.set(directory)
            self.log_message(f"📁 Save location: {directory}")
    
    def check_ffmpeg(self):
        try:
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
            version = result.stdout.split('\n')[0]
            self.log_message(f"✅ {version}")
            return True
        except:
            self.log_message("❌ ffmpeg not found! Install: sudo apt install ffmpeg")
            messagebox.showerror("Missing Dependency", "ffmpeg is required.\n\nInstall with:\nsudo apt install ffmpeg")
            return False
    
    def log_message(self, message):
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.root.update()
    
    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a M3U8 URL")
            return
        
        if not re.match(r'^https?://', url):
            messagebox.showerror("Error", "Invalid URL format. Must start with http:// or https://")
            return
        
        filename = self.filename_entry.get().strip()
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"m3u8_video_{timestamp}.mp4"
        
        if not filename.endswith('.mp4'):
            filename += '.mp4'
        
        save_path = Path(self.location_var.get()) / filename
        
        self.download_btn.config(state='disabled')
        self.progress.start()
        
        thread = threading.Thread(target=self.download_video, args=(url, str(save_path)))
        thread.start()
    
    def download_video(self, url, save_path):
        referer = self.referer_entry.get().strip()
        user_agent = self.ua_entry.get().strip()
        
        self.log_message(f"\n{'='*50}")
        self.log_message(f"🎬 Starting download...")
        self.log_message(f"📋 URL: {url}")
        if referer:
            self.log_message(f"🔗 Referer: {referer}")
        if user_agent:
            self.log_message(f"🌐 User-Agent: {user_agent}")
        self.log_message(f"💾 Save to: {save_path}")
        self.log_message(f"{'='*50}\n")
        
        # Build headers
        headers = []
        if referer:
            headers.append(f"Referer: {referer}")
        if user_agent:
            headers.append(f"User-Agent: {user_agent}")
        
        # Build ffmpeg command
        cmd = ['ffmpeg', '-y', '-i', url]
        if headers:
            cmd.extend(['-headers', '\r\n'.join(headers)])
        cmd.extend(['-c', 'copy', '-bsf:a', 'aac_adtstoasc', save_path])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(save_path) and os.path.getsize(save_path) > 0:
                self.root.after(0, self.download_success, save_path)
            else:
                error_msg = result.stderr if result.stderr else "Unknown error"
                self.root.after(0, self.download_failure, error_msg)
        except Exception as e:
            self.root.after(0, self.download_failure, str(e))
    
    def download_success(self, save_path):
        self.progress.stop()
        self.download_btn.config(state='normal')
        
        size = os.path.getsize(save_path) / (1024 * 1024)
        self.log_message(f"\n{'='*50}")
        self.log_message(f"✅ DOWNLOAD COMPLETE!")
        self.log_message(f"📄 File: {os.path.basename(save_path)}")
        self.log_message(f"💾 Size: {size:.2f} MB")
        self.log_message(f"📍 Location: {save_path}")
        self.log_message(f"{'='*50}")
        
        if messagebox.askyesno("Success", f"Download complete!\n\nFile size: {size:.2f} MB\n\nOpen folder?"):
            subprocess.run(['xdg-open', os.path.dirname(save_path)])
    
    def download_failure(self, error_msg):
        self.progress.stop()
        self.download_btn.config(state='normal')
        
        self.log_message(f"\n{'='*50}")
        self.log_message(f"❌ DOWNLOAD FAILED!")
        self.log_message(f"Error: {error_msg[:500]}")
        self.log_message(f"{'='*50}")
        self.log_message(f"\n💡 Troubleshooting tips:")
        self.log_message(f"   1. Verify the M3U8 URL is correct")
        self.log_message(f"   2. Try adding the Referer URL from the source webpage")
        self.log_message(f"   3. The stream may be protected or expired")
        
        messagebox.showerror("Download Failed", "Could not download the video.\n\nCheck the status window for details.")

def main():
    root = tk.Tk()
    app = M3U8DownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
