#!/usr/bin/env python3
"""
VidsDL CLI - YouTube Video Downloader
Usage: vidsdl-cli <URL> [--quality 1080] [--format mp4]
"""

import sys
import os
import argparse
import yt_dlp
from datetime import datetime

def download_video(url, quality='1080', format_type='mp4'):
    """Download video with specified quality and format"""
    
    print(f"🎬 VidsDL CLI - Downloading...")
    print(f"📺 URL: {url}")
    print(f"📏 Quality: {quality}p")
    print(f"📦 Format: {format_type.upper()}")
    print()
    
    # Downloads folder
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    if not os.path.exists(downloads_folder):
        os.makedirs(downloads_folder)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_template = os.path.join(downloads_folder, f'video_{timestamp}.%(ext)s')
    
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
        }
    else:
        # Check if vertical video (short)
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl_check:
                info = ydl_check.extract_info(url, download=False)
                width = info.get('width', 0)
                height = info.get('height', 0)
                is_vertical = height > width if (width and height) else False
                
                if is_vertical:
                    print(f"📱 Short detected! Forcing max quality...")
                    quality = '2160'
        except:
            pass
        
        format_string = f'bestvideo[height<={quality}]+bestaudio[ext=m4a]/bestvideo[height<={quality}]+bestaudio/best'
        
        ydl_opts = {
            'outtmpl': output_template,
            'format': format_string,
            'merge_output_format': format_type,
            'extractor_args': {
                'youtube': {
                    'player_client': ['android_sdkless', 'web_safari'],
                }
            },
        }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Fix extension
            if is_audio_only:
                base = os.path.splitext(filename)[0]
                filename = base + '.mp3'
            else:
                if not filename.endswith(f'.{format_type}'):
                    base = os.path.splitext(filename)[0]
                    filename = base + f'.{format_type}'
            
            # Check for actual file
            if not os.path.exists(filename):
                base = os.path.splitext(filename)[0]
                for ext in [f'.{format_type}', '.mp4', '.webm', '.mkv', '.m4a', '.mp3']:
                    test_file = base + ext
                    if os.path.exists(test_file):
                        filename = test_file
                        break
            
            # Get video title
            video_title = info.get('title', 'video')
            safe_title = "".join(c for c in video_title if c.isalnum() or c in (' ', '-', '_')).rstrip()[:50]
            
            # Get actual resolution
            actual_width = info.get('width', 'unknown')
            actual_height = info.get('height', 'unknown')
            
            if actual_width != 'unknown' and actual_height != 'unknown':
                resolution_str = f"{actual_width}x{actual_height}"
            else:
                resolution_str = f"{quality}p"
            
            final_filename = f"{safe_title}_{resolution_str}.{format_type}" if not is_audio_only else f"{safe_title}.mp3"
            destination = os.path.join(downloads_folder, final_filename)
            
            # Move file
            if os.path.exists(filename):
                os.rename(filename, destination)
                print()
                print(f"✅ Download complete!")
                print(f"📁 Saved to: {destination}")
                return True
            else:
                print(f"❌ Error: File not found")
                return False
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='VidsDL CLI - YouTube Video Downloader',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  vidsdl-cli https://youtube.com/watch?v=...
  vidsdl-cli https://youtube.com/watch?v=... --quality 720
  vidsdl-cli https://youtube.com/watch?v=... --format mp3
  vidsdl-cli https://youtube.com/watch?v=... --quality 1080 --format webm
        """
    )
    
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('--quality', '-q', default='1080', 
                        choices=['360', '480', '720', '1080', '1440', '2160'],
                        help='Video quality (default: 1080)')
    parser.add_argument('--format', '-f', default='mp4',
                        choices=['mp4', 'webm', 'mov', 'mp3'],
                        help='Output format (default: mp4)')
    
    args = parser.parse_args()
    
    success = download_video(args.url, args.quality, args.format)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
