import sys
import os

# Add the 'server' directory to the Python module search path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "server"))

from app.downloader import download_video, fetch_formats, select_best_format

# Test URL
#url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
url = "https://www.youtube.com/watch?v=0mAesfFt4us"

# Fetch all formats
formats = fetch_formats(url)

# Part 1: List all available formats
print("Listing all available formats:")
for f in formats:
    print(f"ID: {f['format_id']}, Resolution: {f.get('height', 'N/A')}p, FPS: {f.get('fps', 'N/A')}, Audio: {'yes' if f.get('acodec') != 'none' else 'no'}")

# Part 2: Select the best video and audio formats
print("\nSelecting the best formats:")
best_video, best_audio = select_best_format(formats)
print(f"Best Video Format: {best_video}, Best Audio Format: {best_audio}")

result = download_video(url, quality="4320p")  # Example: 8K
print(result)