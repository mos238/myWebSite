from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
import uuid
import subprocess

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-info', methods=['POST'])
def get_video_info():
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
    data = request.json
    url = data.get('url')
    referer = data.get('referer', '')
    
    if not url:
        return jsonify({'success': False, 'error': 'No URL provided'}), 400
    
    filename = f"m3u8_video_{uuid.uuid4().hex[:8]}.mp4"
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    
    try:
        cmd = ['ffmpeg', '-y']
        
        # Add referer header if provided
        if referer:
            cmd.extend(['-headers', f'Referer: {referer}'])
        
        cmd.extend(['-i', url, '-c', 'copy', '-bsf:a', 'aac_adtstoasc', filepath])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            return send_file(
                filepath,
                as_attachment=True,
                download_name=filename
            )
        else:
            error_msg = result.stderr if result.stderr else "Unknown error"
            return jsonify({'success': False, 'error': f'FFmpeg error: {error_msg[:200]}'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
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
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
