import asyncio, yt_dlp
from typing import Union
from pyrogram.types import Audio, Voice, Video, VideoNote
from pytgcalls.types.input_stream import InputAudioStream, InputVideoStream
from pytgcalls.types.input_stream.quality import AudioQuality, VideoQuality
from youtubesearchpython.__future__ import VideosSearch
from VenomX import config

def get_audio_name(audio: Union[Audio, Voice]):
    try:
        return audio.file_unique_id + "." + (audio.file_name.split(".")[-1] if not isinstance(audio, Voice) else "ogg")
    except:
        return audio.file_unique_id + ".ogg"

def get_video_name(video: Union[Video, VideoNote]):
    try:
        return video.file_unique_id + "." + video.file_name.split(".")[-1]
    except:
        return video.file_unique_id + ".mp4"

async def get_media_info(vidid: str, query: str):
    url = f"https://www.youtube.com/watch?v={vidid}" if vidid else None
    search = url if url else query
    results = VideosSearch(search, limit=1)
    for result in (await results.next())["result"]:
        videoid = vidid if vidid else result["id"]
        videourl = url if vidid else result["link"]
    return [videoid, videourl]

async def get_stream_link(link: str):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp", "-g", "-f", "bestvideo+bestaudio/best",
        "--cookies", "cookies.txt", f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    links = stdout.decode().split("\n")
    return links[0], links[1]

async def get_media_stream(media, type_: str):
    if type_ == "Audio":
        return InputAudioStream(
            media,
            quality=AudioQuality.STUDIO
        )
    elif type_ == "Video":
        return InputVideoStream(
            media,
            quality=VideoQuality.HD_720p
        )
