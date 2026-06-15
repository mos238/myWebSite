from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
import uuid
import subprocess

app = Flask(__name__)

# Create downloads folder
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-info', methods=['POST'])
def get_video_info():
    """Get video information for YouTube"""
    data = request.json
    url = data.get('url')
    
    try:
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = []
            for f in info['formats']:
                if f.get('height') and f.get('ext') in ['mp4', 'webm']:
                    formats.append({
                        'quality': f"{f['height']}p",
                        'format_id': f['format_id'],
                        'ext': f['ext'],
                        'filesize': f.get('filesize', 0)
                    })
            
            return jsonify({
                'success': True,
                'title': info['title'],
                'thumbnail': info['thumbnail'],
                'duration': info['duration'],
                'formats': formats
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download-m3u8', methods=['POST'])
def download_m3u8():
    """Download M3U8/HLS video stream"""
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'success': False, 'error': 'No URL provided'})
    
    filename = f"m3u8_video_{uuid.uuid4().hex[:8]}.mp4"
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    
    try:
        # Use ffmpeg to download m3u8 stream
        cmd = ['ffmpeg', '-i', url, '-c', 'copy', '-bsf:a', 'aac_adtstoasc', filepath]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(filepath):
            return send_file(
                filepath,
                as_attachment=True,
                download_name=filename
            )
        else:
            return jsonify({'success': False, 'error': 'Failed to download M3U8 stream'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        # Clean up
        if os.path.exists(filepath):
            os.remove(filepath)

@app.route('/download', methods=['POST'])
def download_video():
    """Download YouTube video"""
    data = request.json
    url = data.get('url')
    format_id = data.get('format_id')
    
    filename = f"{uuid.uuid4().hex}.mp4"
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    
    try:
        ydl_opts = {
            'format': format_id,
            'outtmpl': filepath,
            'quiet': True,
            'no_warnings': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        return send_file(
            filepath,
            as_attachment=True,
            download_name=f"youtube_video_{uuid.uuid4().hex[:8]}.mp4"
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
