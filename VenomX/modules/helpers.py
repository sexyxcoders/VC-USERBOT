import asyncio
import os
import yt_dlp
import ssl
import certifi

# Ensure root CA certificates are used (fix Heroku SSL issues)
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())

# Make sure downloads folder exists
os.makedirs("downloads", exist_ok=True)

async def download_media_file(link: str, type: str):
    """
    Downloads audio or video from YouTube or other supported sites asynchronously.
    Returns the file path after download.
    """
    loop = asyncio.get_running_loop()

    # Configure yt-dlp options
    if type == "Audio":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "quiet": True,
            "no_warnings": True,
            "cookiefile": "cookies.txt",
        }
    elif type == "Video":
        ydl_opts = {
            "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "quiet": True,
            "no_warnings": True,
            "cookiefile": "cookies.txt",
        }

    ydl = yt_dlp.YoutubeDL(ydl_opts)

    # Extract info first in executor (blocking operation)
    info = await loop.run_in_executor(None, lambda: ydl.extract_info(link, download=False))
    file_path = os.path.join("downloads", f"{info['id']}.{info['ext']}")

    # If file already exists, return it
    if os.path.exists(file_path):
        return file_path

    # Download media in executor
    await loop.run_in_executor(None, lambda: ydl.download([link]))
    return file_path
