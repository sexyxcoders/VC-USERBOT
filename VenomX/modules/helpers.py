import asyncio, os, yt_dlp, ssl, certifi

ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
os.makedirs("downloads", exist_ok=True)

async def download_media_file(link: str, type_: str):
    loop = asyncio.get_running_loop()
    if type_ == "Audio":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "quiet": True,
            "cookiefile": "cookies.txt"
        }
    else:
        ydl_opts = {
            "format": "(bestvideo[height<=?720][ext=mp4]+bestaudio[ext=m4a]/best)",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "quiet": True,
            "cookiefile": "cookies.txt"
        }

    ydl = yt_dlp.YoutubeDL(ydl_opts)
    info = await loop.run_in_executor(None, lambda: ydl.extract_info(link, download=False))
    file_path = os.path.join("downloads", f"{info['id']}.{info['ext']}")
    if os.path.exists(file_path):
        return file_path
    await loop.run_in_executor(None, lambda: ydl.download([link]))
    return file_path
