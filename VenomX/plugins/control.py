import re
from pyrogram import filters
from VenomX.modules.clients import app, call, cdz, eor
from VenomX.modules.streams import get_media_stream
from VenomX.modules.queues import add_to_queue, get_from_queue, is_queue_empty
from VenomX.modules.streams import download_media_file, get_media_info
from pytgcalls.types.input_stream import AudioPiped, VideoPiped

# -------------------------------
# Play / Stream command
# -------------------------------
@app.on_message(cdz(["play", "ply", "vplay", "vply"]) & ~filters.private)
async def start_stream(client, message):
    if message.sender_chat:
        return

    aux = await eor(message, "🔄 Processing ...")
    chat_id = message.chat.id
    replied = message.reply_to_message
    command = str(message.command[0]).lower()

    # Determine type
    audiostream = replied.audio or replied.voice if replied else None
    videostream = replied.video or replied.document if replied else None

    if audiostream:
        media = await client.download_media(replied)
        type_ = "Audio"
    elif videostream:
        media = await client.download_media(replied)
        type_ = "Video"
    else:
        if len(message.command) < 2:
            return await aux.edit("❌ Give a query or reply to a file to stream!")

        query = message.text.split(None, 1)[1]
        vidid = None
        if "https://" in query:
            base = r"(?:https?:)?(?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube(?:\-nocookie)?\.(?:[A-Za-z]{2,4}|[A-Za-z]{2,3}\.[A-Za-z]{2})\/)?(?:shorts\/|live\/)?(?:watch|embed\/|vi?\/)*(?:\?[\w=&]*vi?=)?([^#&\?\/]{11}).*$"
            resu = re.findall(base, query)
            vidid = resu[0] if resu else None

        results = await get_media_info(vidid, query)
        link = str(results[1])
        type_ = "Video" if command.startswith("v") else "Audio"
        media = await download_media_file(link, type_)

    # Try to get active call
    try:
        call_obj = await call.get_call(chat_id)
        if call_obj is None or not call_obj.is_active:
            # Join VC
            stream = AudioPiped(media) if type_ == "Audio" else VideoPiped(media)
            await call.join_group_call(chat_id, stream)
            await add_to_queue(chat_id, media=media, type=type_)
            return await aux.edit("▶ Streaming started!")
        else:
            # Already in VC, add to queue
            position = await add_to_queue(chat_id, media=media, type=type_)
            return await aux.edit(f"✅ Added to queue at position {position}")
    except Exception as e:
        print(f"❌ Error in streaming: {e}")
        return await aux.edit("❌ Could not start streaming. Try again!")
