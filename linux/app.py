import webview
import threading
import os
import sys
import time
import shutil
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import tempfile
from datetime import datetime

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
CORS(app)
TEMP_DIR = tempfile.gettempdir()

# Downloads folder - Linux (user's Downloads folder)
DOWNLOADS_FOLDER = os.path.join(os.path.expanduser('~'), 'Downloads')

# Create downloads folder if it doesn't exist
if not os.path.exists(DOWNLOADS_FOLDER):
    os.makedirs(DOWNLOADS_FOLDER)

def format_duration(seconds):
    if seconds is None:
        return "N/A"
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"

@app.route('/')
def home():
    html_path = os.path.join(BASE_DIR, 'index.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/info', methods=['POST'])
def get_info():
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({'error': 'URL não fornecida'}), 400
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'android'],
                }
            },
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Detect if it's a short (vertical video)
            width = info.get('width', 0)
            height = info.get('height', 0)
            is_vertical = height > width if (width and height) else False
            
            # Get all available formats to check resolutions
            available_heights = set()
            if 'formats' in info:
                for fmt in info['formats']:
                    fmt_height = fmt.get('height')
                    if fmt_height and fmt_height >= 360:  # Only resolutions 360p+
                        available_heights.add(fmt_height)
            
            return jsonify({
                'title': info.get('title', 'Título não disponível'),
                'duration': format_duration(info.get('duration')),
                'thumbnail': info.get('thumbnail', ''),
                'uploader': info.get('uploader', 'Desconhecido'),
                'view_count': info.get('view_count', 0),
                'upload_date': info.get('upload_date', 'N/A'),
                'is_vertical': is_vertical,
                'width': width,
                'height': height,
                'available_heights': sorted(list(available_heights), reverse=True)
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download_video():
    filename = None
    try:
        data = request.get_json()
        url = data.get('url')
        quality = data.get('quality', '1080')
        format_type = data.get('format', 'mp4')
        
        if not url:
            return jsonify({'error': 'URL não fornecida'}), 400
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_template = os.path.join(TEMP_DIR, f'video_{timestamp}.%(ext)s')
        is_audio_only = format_type == 'mp3'
        
        if is_audio_only:
            ydl_opts = {
                'outtmpl': output_template,
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': False,
                'no_warnings': False,
            }
        else:
            # FUCK IT - Just use "best" for now since YouTube is being a bitch
            # User can select quality but we'll try to get closest to it
            # Force m4a audio for better Windows compatibility (not opus)
            format_string = f'bestvideo[height<={quality}]+bestaudio[ext=m4a]/bestvideo[height<={quality}]+bestaudio/best'
            merge_format = format_type
            print(f"[FORMAT] Using format: best video <={quality}p + m4a audio")
            
            ydl_opts = {
                'outtmpl': output_template,
                'format': format_string,
                'merge_output_format': merge_format,
                'quiet': False,
                'no_warnings': False,
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': format_type,
                }] if format_type == 'mov' else [],
                # Add ignore errors for unavailable formats
                'ignore_no_formats_error': False,
            }
        
        ydl_opts.update({
            'nocheckcertificate': True,
            'no_color': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'referer': 'https://www.youtube.com/',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
            },
            'extractor_args': {
                'youtube': {
                    # Only use web client when cookies are present
                    'player_client': ['web'],
                    'player_skip': ['webpage', 'configs'],
                }
            },
            'geo_bypass': True,
            'age_limit': None,
        })
        
        # Check for cookies file and use it if available
        cookies_file = os.path.join(BASE_DIR, 'cookies.txt')
        if os.path.exists(cookies_file):
            ydl_opts['cookiefile'] = cookies_file
            # Use web client with cookies
            ydl_opts['extractor_args']['youtube']['player_client'] = ['web']
            print(f"[COOKIE] Using cookies from: {cookies_file}")
        else:
            # Without cookies, use android_sdkless which doesn't need PO tokens
            ydl_opts['extractor_args']['youtube']['player_client'] = ['android_sdkless', 'web_safari']
            print(f"[WARN] No cookies found - using android_sdkless client")
        
        print(f"> Download: {url}")
        print(f"[INFO] Quality: {quality}p | Format: {format_type.upper()}")
        
        # SHORTS FIX: If vertical video, force max resolution to get best available
        # Check video info to see if it's vertical
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl_check:
                check_info = ydl_check.extract_info(url, download=False)
                check_width = check_info.get('width', 0)
                check_height = check_info.get('height', 0)
                is_vertical = check_height > check_width if (check_width and check_height) else False
                
                if is_vertical:
                    original_quality = quality
                    quality = '2160'  # Always force max for shorts
                    print(f"[SHORT DETECTED] Forcing {original_quality}p -> {quality}p to get best available")
        except:
            pass  # If check fails, continue with original quality
        
        # First, list available formats for debugging
        print("\n[CHECK] Checking available formats...")
        try:
            with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl_test:
                info_test = ydl_test.extract_info(url, download=False)
                if 'formats' in info_test:
                    print(f"[OK] Found {len(info_test['formats'])} formats available")
                    # Show some format details
                    for fmt in info_test['formats'][:5]:  # Show first 5
                        height = fmt.get('height', 'N/A')
                        ext = fmt.get('ext', 'N/A')
                        format_id = fmt.get('format_id', 'N/A')
                        print(f"   - ID: {format_id} | {height}p | {ext}")
        except Exception as list_error:
            print(f"[WARN] Could not list formats: {list_error}")
        print()
        
        # Try to download with specific format
        download_success = False
        for attempt in range(2):
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    download_success = True
                    break
            except Exception as download_error:
                print(f"\n[ERROR] Attempt {attempt + 1} failed: {str(download_error)[:100]}")
                if attempt == 0:
                    # First attempt failed, try with simple "best"
                    print(f"[WARN] Trying fallback with 'best' format...")
                    ydl_opts['format'] = 'best'
                    continue
                else:
                    # Both attempts failed
                    print(f"[ERROR] All attempts failed!")
                    raise download_error
        
        if not download_success:
            raise Exception("Download failed after all attempts")
            
            if is_audio_only:
                base = os.path.splitext(filename)[0]
                filename = base + '.mp3'
            else:
                if not filename.endswith(f'.{format_type}'):
                    base = os.path.splitext(filename)[0]
                    filename = base + f'.{format_type}'
            
            if not os.path.exists(filename):
                base = os.path.splitext(filename)[0]
                for ext in [f'.{format_type}', '.mp4', '.webm', '.mkv', '.m4a', '.mp3']:
                    test_file = base + ext
                    if os.path.exists(test_file):
                        filename = test_file
                        break
            
            if not os.path.exists(filename):
                raise Exception('Arquivo não foi criado')
            if os.path.getsize(filename) == 0:
                raise Exception('Arquivo vazio')
        
        # Get video title and create safe filename
        video_title = info.get('title', 'video')
        safe_title = "".join(c for c in video_title if c.isalnum() or c in (' ', '-', '_')).rstrip()[:50]
        
        # Log actual downloaded resolution
        actual_width = info.get('width', 'unknown')
        actual_height = info.get('height', 'unknown')
        print(f"[INFO] Actual downloaded resolution: {actual_width}x{actual_height}")
        
        # Use ACTUAL resolution in filename instead of requested
        if actual_width != 'unknown' and actual_height != 'unknown':
            resolution_str = f"{actual_width}x{actual_height}"
        else:
            resolution_str = f"{quality}p"
        
        final_filename = f"{safe_title}_{resolution_str}.{format_type}" if not is_audio_only else f"{safe_title}.mp3"
        
        # Copy to Downloads folder (more reliable than move)
        destination = os.path.join(DOWNLOADS_FOLDER, final_filename)
        
        # If file exists, add number
        counter = 1
        base_dest = destination
        while os.path.exists(destination):
            name, ext = os.path.splitext(base_dest)
            destination = f"{name}_{counter}{ext}"
            counter += 1
        
        # Copy file
        print(f"[SAVE] Copying to: {destination}")
        shutil.copy2(filename, destination)
        print(f"[OK] Saved to: {destination}")
        
        # Clean up temp file
        try:
            os.remove(filename)
        except:
            pass
        
        # Return success
        return jsonify({
            'success': True,
            'message': 'Download concluído!',
            'file_path': destination,
            'file_name': os.path.basename(destination)
        })
        
    except Exception as e:
        print(f"[ERROR] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Clean up on error
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass
        
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

def start_server():
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

def main():
    print("=" * 60)
    print("VidsDL v2.1 - Starting...")
    print(f"Downloads will be saved to: {DOWNLOADS_FOLDER}")
    print("=" * 60)
    
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(1)
    
    window = webview.create_window(
        'VidsDL', 
        'http://127.0.0.1:5000',  # Use HTTP not HTTPS
        width=800, 
        height=900,
        resizable=True
    )
    webview.start(debug=False)

if __name__ == '__main__':
    main()
