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
    loop = asyncio.get_running_loop()

    if type == "Audio":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "geo_bypass": True,
            "quiet": True,
            "no_warnings": True,
            "cookiefile": "cookies.txt",
        }

    elif type == "Video":
        ydl_opts = {
            "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "geo_bypass": True,
            "quiet": True,
            "no_warnings": True,
            "cookiefile": "cookies.txt",
        }

    ydl = yt_dlp.YoutubeDL(ydl_opts)

    # Extract video info in executor
    info = await loop.run_in_executor(None, lambda: ydl.extract_info(link, download=False))
    file_path = os.path.join("downloads", f"{info['id']}.{info['ext']}")

    if os.path.exists(file_path):
        return file_path

    # Download the media
    await loop.run_in_executor(None, lambda: ydl.download([link]))
    return file_path
