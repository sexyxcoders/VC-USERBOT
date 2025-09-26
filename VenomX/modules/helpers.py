import asyncio
import os
import yt_dlp
import ssl
import certifi

# Ensure Python/yt-dlp uses updated root CA certificates
ssl._create_default_https_context = ssl.create_default_context
ssl._create_default_https_context().load_verify_locations(certifi.where())

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

    x = yt_dlp.YoutubeDL(ydl_opts)

    # Extract info synchronously first
    info = await loop.run_in_executor(None, x.extract_info, link, False)
    file = os.path.join("downloads", f"{info['id']}.{info['ext']}")

    if os.path.exists(file):
        return file

    # Download in executor
    await loop.run_in_executor(None, x.download, [link])
    return file
