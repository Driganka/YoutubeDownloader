import sys
import os

# Add the 'server' directory to the Python module search path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "server"))

from app.downloader import download_video, fetch_formats

# Test URL
#url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
url = "https://www.youtube.com/watch?v=0mAesfFt4us"

# Test: Fetch and display formats
print("Available formats:")
formats = fetch_formats(url)
for f in formats:
    print(f"ID: {f['format_id']}, Resolution: {f.get('height', 'N/A')}p, FPS: {f.get('fps', 'N/A')}, Audio: {'yes' if f.get('acodec') != 'none' else 'no'}")


result = download_video(url, quality="4320p")  # Example: 8K
print(result)