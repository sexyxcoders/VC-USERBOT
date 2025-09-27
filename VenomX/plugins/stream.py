import re

from VenomX import app, call, cdz, eor
from VenomX import add_to_queue
from VenomX import download_media_file
from VenomX import get_media_info, get_media_stream
from pyrogram import filters
from pytgcalls.exceptions import AlreadyJoinedError, GroupCallNotFound
from pytgcalls.exceptions import NoActiveGroupCall


@app.on_message(cdz(["ply", "play", "vply", "vplay"]) & ~filters.private)
async def start_stream(client, message):
    if message.sender_chat:
        return
    aux = await eor(message, "**🔄 Processing ...**")
    chat_id = message.chat.id
    replied = message.reply_to_message
    audiostream = ((replied.audio or replied.voice) if replied else None)
    videostream = ((replied.video or replied.document) if replied else None)
    command = str(message.command[0][0])

    if audiostream:
        media = await client.download_media(replied)
        type = "Audio"
    elif videostream:
        media = await client.download_media(replied)
        type = "Video"
    else:
        if len(message.command) < 2:
            return await aux.edit(
                "**🥀 Give Me Some Query To\nStream Audio Or Video❗...**"
            )
        query = message.text.split(None, 1)[1]
        vidid = None
        if "https://" in query:
            base = r"(?:https?:)?(?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube(?:\-nocookie)?\.(?:[A-Za-z]{2,4}|[A-Za-z]{2,3}\.[A-Za-z]{2})\/)?(?:shorts\/|live\/)?(?:watch|embed\/|vi?\/)*(?:\?[\w=&]*vi?=)?([^#&\?\/]{11}).*$"
            resu = re.findall(base, query)
            vidid = resu[0] if resu else None
        results = await get_media_info(vidid, query)
        link = str(results[1])
        type = "Video" if command.startswith("v") else "Audio"
        media = await download_media_file(link, type)

    stream = await get_media_stream(media, type)

    # ---------------- PyTgCalls v2 safe handling ----------------
    try:
        # Try to join or change stream; v2 raises exceptions if group call exists
        await call.join_group_call(chat_id, stream, auto_start=True)
        await add_to_queue(chat_id, media=media, type=type)
        await aux.edit("**Streaming Started ....**")
    except AlreadyJoinedError:
        # Already in VC → just change stream or add to queue
        await call.change_stream(chat_id, stream)
        position = await add_to_queue(chat_id, media=media, type=type)
        await aux.edit(f"**Added to Queue At {position}**")
    except NoActiveGroupCall:
        await aux.edit("**No Active VC !**")
    except Exception as e:
        print(f"Error: {e}")
        await aux.edit("**Please Try Again !**")
