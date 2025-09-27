import asyncio
from typing import Union
from pyrogram.types import Audio, Voice, Video, VideoNote
from youtubesearchpython.__future__ import VideosSearch
from pytgcalls.types import MediaStream
from pytgcalls.types import AudioQuality, VideoQuality


# -----------------------------
# Helper Functions for Filenames
# -----------------------------
def get_audio_name(audio: Union[Audio, Voice]) -> str:
    """
    Returns a safe filename for Audio or Voice messages.
    """
    try:
        ext = "ogg" if isinstance(audio, Voice) else audio.file_name.split(".")[-1]
        file_name = f"{audio.file_unique_id}.{ext}"
    except Exception:
        file_name = f"{audio.file_unique_id}.ogg"
    return file_name


def get_video_name(video: Union[Video, VideoNote]) -> str:
    """
    Returns a safe filename for Video or VideoNote messages.
    """
    try:
        ext = video.file_name.split(".")[-1]
        file_name = f"{video.file_unique_id}.{ext}"
    except Exception:
        file_name = f"{video.file_unique_id}.mp4"
    return file_name


# -----------------------------
# YouTube Helpers
# -----------------------------
async def get_media_info(vidid: str = None, query: str = None) -> list[str]:
    """
    Returns [videoid, videourl] for a YouTube video based on ID or search query.
    """
    url = f"https://www.youtube.com/watch?v={vidid}" if vidid else None
    search_term = url if url else query

    results = VideosSearch(search_term, limit=1)
    for result in (await results.next())["result"]:
        videoid = vidid if vidid else result["id"]
        videourl = url if url else result["link"]
        return [videoid, videourl]
    
    return [None, None]


async def get_stream_link(link: str) -> tuple[str, str]:
    """
    Returns direct video and audio URLs from a YouTube link using yt-dlp.
    """
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
    lines = stdout.decode().splitlines()
    if len(lines) < 2:
        raise Exception(f"Failed to get stream links: {stderr.decode()}")
    return lines[0], lines[1]


# -----------------------------
# PyTgCalls Media Stream
# -----------------------------
async def get_media_stream(media: str, type: str) -> MediaStream:
    """
    Returns a MediaStream object for PyTgCalls.
    type: "audio" or "video"
    """
    type_lower = type.lower()
    if type_lower == "audio":
        # Audio-only stream
        stream = MediaStream(
            media_path=media,
            audio_parameters=AudioQuality.STUDIO,
        )
    elif type_lower == "video":
        # Audio + Video stream
        stream = MediaStream(
            media_path=media,
            audio_parameters=AudioQuality.STUDIO,
            video_parameters=VideoQuality.HD_720p,
        )
    else:
        raise ValueError("Invalid type: must be 'audio' or 'video'")
    return stream