import asyncio, yt_dlp, os
from typing import Union
from pyrogram.types import Audio, Voice, Video, VideoNote
from pytgcalls.types.input_stream import InputAudioStream, InputVideoStream
from pytgcalls.types.input_stream.quality import HighQualityAudio, HighQualityVideo
from youtubesearchpython.__future__ import VideosSearch

os.makedirs("downloads", exist_ok=True)

# -------------------------------
# File name helpers
# -------------------------------
def get_audio_name(audio: Union[Audio, Voice]):
    try:
        ext = "ogg" if isinstance(audio, Voice) else audio.file_name.split(".")[-1]
        return f"{audio.file_unique_id}.{ext}"
    except:
        return f"{audio.file_unique_id}.ogg"

def get_video_name(video: Union[Video, VideoNote]):
    try:
        return f"{video.file_unique_id}.{video.file_name.split('.')[-1]}"
    except:
        return f"{video.file_unique_id}.mp4"

# -------------------------------
# YouTube search
# -------------------------------
async def get_media_info(vidid: str = None, query: str = None):
    url = f"https://www.youtube.com/watch?v={vidid}" if vidid else None
    search = url if url else query
    results = VideosSearch(search, limit=1)
    for result in (await results.next())["result"]:
        videoid = vidid if vidid else result["id"]
        videourl = url if url else result["link"]
    return videoid, videourl

# -------------------------------
# Get stream link
# -------------------------------
async def get_stream_link(link: str):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp", "-g", "-f", "bestvideo+bestaudio/best", link,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, _ = await proc.communicate()
    return stdout.decode().split('\n')[:2]

# -------------------------------
# PyTgCalls stream wrapper
# -------------------------------
async def get_media_stream(media: str, type_: str):
    if type_ == "Audio":
        return InputAudioStream(
            media,
            HighQualityAudio()
        )
    elif type_ == "Video":
        return InputVideoStream(
            media,
            HighQualityVideo(),
            HighQualityAudio()
        )
