from flask import Flask, render_template, request, send_file, jsonify
from flask_cors import CORS
import yt_dlp
import os
import uuid
import subprocess
import re

app = Flask(__name__)
CORS(app)

DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def clean_youtube_url(url):
    if 'youtu.be' in url:
        match = re.search(r'youtu\.be/([a-zA-Z0-9_-]+)', url)
        if match:
            video_id = match.group(1)
            return f'https://www.youtube.com/watch?v={video_id}'
    if 'youtube.com' in url:
        base_url = re.sub(r'[?&](si|feature|list|index|pp|is)=[^&]*', '', url)
        return base_url
    return url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-info', methods=['POST'])
def get_video_info():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'success': False, 'error': 'No URL provided'}), 400
    
    url = clean_youtube_url(url)
    
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = []
            for f in info.get('formats', []):
                if f.get('height') and f.get('ext') in ['mp4', 'webm']:
                    formats.append({
                        'quality': f"{f['height']}p",
                        'format_id': f['format_id'],
                        'ext': f['ext'],
                        'filesize': f.get('filesize', 0)
                    })
            
            formats.sort(key=lambda x: int(x['quality'].replace('p', '')), reverse=True)
            
            return jsonify({
                'success': True,
                'title': info.get('title', 'Unknown'),
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration', 0),
                'formats': formats[:10]
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/download-m3u8', methods=['POST'])
def download_m3u8():
    data = request.json
    url = data.get('url')
    referer = data.get('referer', '')
    
    if not url:
        return jsonify({'success': False, 'error': 'No URL provided'}), 400
    
    filename = f"m3u8_video_{uuid.uuid4().hex[:8]}.mp4"
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    
    try:
        # Build ffmpeg command
        cmd = ['ffmpeg', '-y']
        
        # Add headers
        if referer:
            cmd.extend(['-headers', f'Referer: {referer}\r\n'])
        
        cmd.extend([
            '-user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            '-i', url,
            '-c', 'copy',
            '-bsf:a', 'aac_adtstoasc',
            filepath
        ])
        
        # Run ffmpeg
        process = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        # Check if download succeeded
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            file_size = os.path.getsize(filepath) / (1024 * 1024)
            return send_file(
                filepath,
                as_attachment=True,
                download_name=filename,
                mimetype='video/mp4'
            )
        else:
            # Get the actual error message
            error_msg = process.stderr if process.stderr else "Unknown error"
            # Extract useful error from ffmpeg output
            if "404" in error_msg:
                error_msg = "Stream not found (404) - URL may be invalid or expired"
            elif "403" in error_msg:
                error_msg = "Access forbidden (403) - Try adding the correct Referer URL"
            elif "Invalid data" in error_msg:
                error_msg = "Invalid M3U8 stream - URL may be incorrect"
            else:
                # Get last line of error
                lines = error_msg.strip().split('\n')
                error_msg = lines[-1] if lines else error_msg
            
            return jsonify({'success': False, 'error': error_msg}), 500
            
    except subprocess.TimeoutExpired:
        return jsonify({'success': False, 'error': 'Download timeout (5 minutes)'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        # Clean up
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    format_id = data.get('format_id')
    
    if not url:
        return jsonify({'success': False, 'error': 'No URL provided'}), 400
    
    url = clean_youtube_url(url)
    
    filename = f"{uuid.uuid4().hex}.mp4"
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    
    try:
        ydl_opts = {
            'format': format_id,
            'outtmpl': filepath,
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            return send_file(
                filepath,
                as_attachment=True,
                download_name=f"youtube_video_{uuid.uuid4().hex[:8]}.mp4",
                mimetype='video/mp4'
            )
        else:
            return jsonify({'success': False, 'error': 'Download failed - file not created'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
