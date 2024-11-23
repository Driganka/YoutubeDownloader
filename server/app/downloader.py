import yt_dlp
import os

# Configuration for yt-dlp
YDL_OPTIONS = {
    'format': 'bestvideo+bestaudio/best',  # Download best quality video + audio
    'outtmpl': 'static/%(title)s.%(ext)s',  # Save file in 'static' folder
    'merge_output_format': 'mp4',          # Merge video and audio into MP4 format
    'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4',           # Ensure output format is MP4
    }],
}

# Step 1:- Retrieve All Available Formats
# We will use yt_dlp to fetch detailed information about all available formats for the provided URL without downloading the video.
# -- Adding a helper function to fetch the formats --
def fetch_formats(url: str) -> list:
    """
    Fetch all available formats for a given video URL.

    Args:
        url (str): YouTube URL
    
    Returns:
        list: List of available formats with details
    """
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', [])
            return formats
    except Exception as e:
        print(f"Error fetching formats: {e}")
        return []



# Step 2 :- Selecting the Best Format
# We will prioritize based on resolution, frame rate, and whether the format has audio.
# -- Adding a helper function to select the best format --
def select_best_format(formats: list) -> tuple:
    """
    Select the best video and audio format based on quality.

    Args:
        formats (list): List of formats fetched from yt-dlp

    Returns:
        tuple: Best video and audio format IDs
    """
    video_formats = [f for f in formats if f.get('vcodec') != 'none']
    audio_formats = [f for f in formats if f.get('acodec') != 'none']

    # Sort video formats by resolution and FPS (highest first)
    video_formats.sort(key=lambda f: (f.get('height', 0), f.get('fps', 0)), reverse=True)

    # Sort audio formats by bitrate (highest first)
    audio_formats.sort(key=lambda f: f.get('abr', 0), reverse=True)

    best_video = video_formats[0] if video_formats else None
    best_audio = audio_formats[0] if audio_formats else None

    return (best_video.get('format_id') if best_video else None,
            best_audio.get('format_id') if best_audio else None)



# Step 3 :- Merge Video and Audio
# If the best video and audio are separate formats, we need to download them and use ffmpeg to merge.
# Core downloader function
def download_video(url: str) -> dict:
    """
    Download the highest quality video and merge with the best audio.

    Args:
        url (str): YouTube URL
    
    Returns:
        dict: Information about the downloaded file
    """
    formats = fetch_formats(url)
    best_video, best_audio = select_best_format(formats)

    if not best_video or not best_audio:
        return {'error': 'No suitable formats found'}

    options = YDL_OPTIONS.copy()
    options['format'] = f"{best_video}+{best_audio}"

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)

            return {
                'title': info_dict.get('title', 'Unknown Title'),
                'file_path': file_path,
                'duration': info_dict.get('duration', 0),
                'thumbnail': info_dict.get('thumbnail'),
                'uploader': info_dict.get('uploader', 'Unknown Uploader'),
            }
    except Exception as e:
        return {'error': str(e)}



# Utility to clean up downloaded files (optional)
def cleanup_downloads():
    """
    Remove all files in the static folder.
    """
    folder = 'static'
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
