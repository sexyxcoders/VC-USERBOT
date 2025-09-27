import os
import asyncio
import yt_dlp

# modules/helpers.py
from py_tgcalls.types import InputAudioStream as AudioPiped
from py_tgcalls.types import InputVideoStream as VideoPiped

# Ensure downloads folder exists
os.makedirs("downloads", exist_ok=True)


async def download_media_file(link: str, type: str):
    loop = asyncio.get_running_loop()

    if type == "Audio":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "geo_bypass": True,
            "nocheckcertificate": True,
            "quiet": True,
            "no_warnings": True,
            "cookiefile": "cookies.txt",
        }
    elif type == "Video":
        ydl_opts = {
            "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "geo_bypass": True,
            "nocheckcertificate": True,
            "quiet": True,
            "no_warnings": True,
            "cookiefile": "cookies.txt",
        }
    else:
        raise ValueError("Type must be 'Audio' or 'Video'")

    ydl = yt_dlp.YoutubeDL(ydl_opts)
    info = await loop.run_in_executor(None, lambda: ydl.extract_info(link, download=False))
    file_path = os.path.join("downloads", f"{info['id']}.{info['ext']}")

    if not os.path.exists(file_path):
        await loop.run_in_executor(None, lambda: ydl.download([link]))

    return file_path


async def get_media_stream(media: str, type: str):
    if type == "Audio":
        return AudioPiped(media)
    elif type == "Video":
        return VideoPiped(media)
    else:
        raise ValueError("Invalid type. Must be 'Audio' or 'Video'.")