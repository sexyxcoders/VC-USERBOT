import asyncio
import os
import yt_dlp
import ssl
import certifi
from typing import Union
from pyrogram.types import Audio, Voice, Video, VideoNote
from pytgcalls.types import AudioQuality, VideoQuality
from pytgcalls.types.stream import InputStream, AudioPiped, VideoPiped
from youtubesearchpython.__future__ import VideosSearch
from VenomX import config

# Ensure root CA certificates are used (fix Heroku SSL issues)
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())

# Make sure downloads folder exists
os.makedirs("downloads", exist_ok=True)


def get_audio_name(audio: Union[Audio, Voice]):
    try:
        ext = "ogg" if isinstance(audio, Voice) else audio.file_name.split(".")[-1]
        file_name = f"{audio.file_unique_id}.{ext}"
    except:
        file_name = f"{audio.file_unique_id}.ogg"
    return file_name


def get_video_name(video: Union[Video, VideoNote]):
    try:
        ext = video.file_name.split(".")[-1]
        file_name = f"{video.file_unique_id}.{ext}"
    except:
        file_name = f"{video.file_unique_id}.mp4"
    return file_name


# Get Details Of Youtube Video
async def get_media_info(vidid: str, query: str):
    url = f"https://www.youtube.com/watch?v={vidid}" if vidid else None
    search = url if url else query
    results = VideosSearch(search, limit=1)
    for result in (await results.next())["result"]:
        videoid = vidid if vidid else result["id"]
        videourl = url if url else result["link"]
    return [videoid, videourl]


# Direct Link From YouTube
async def get_stream_link(link: str):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "bestvideo+bestaudio/best",
        "--cookies", "cookies.txt",
        link,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    urls = stdout.decode().split("\n")
    return urls[0], urls[1]


# Stream Using PyTgCalls v3
async def get_media_stream(media, type_: str):
    """
    Returns the correct PyTgCalls InputStream for audio or video.
    """
    if type_ == "Audio":
        return AudioPiped(media, audio_quality=AudioQuality.STANDARD)
    elif type_ == "Video":
        return VideoPiped(media, audio_quality=AudioQuality.STANDARD, video_quality=VideoQuality.Q720P)
