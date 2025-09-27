import re
from VenomX.modules.clients import app, call
from VenomX.modules.helpers import cdz, eor
from VenomX.modules.queues import add_to_queue, get_from_queue, clear_queue, is_queue_empty, task_done
from VenomX.modules.streams import download_media_file, get_media_info, get_media_stream
from pyrogram import filters

# -------------------------------
# Play command
# -------------------------------
@app.on_message(cdz(["play", "ply"]) & ~filters.private)
async def start_stream(client, message):
    if message.sender_chat:
        return
    aux = await eor(message, "🔄 Processing ...")
    chat_id = message.chat.id
    query = message.text.split(None, 1)[1] if len(message.command) > 1 else None

    # Download media
    if "https://" in query:
        media_path = await download_media_file(query, "Audio")
        type_ = "Audio"
    else:
        vidid, link = await get_media_info(None, query)
        media_path = await download_media_file(link, "Audio")
        type_ = "Audio"

    # Join VC or add to queue
    try:
        call_obj = await call.get_call(chat_id)
        if call_obj.status == "not_playing":
            stream = await get_media_stream(media_path, type_)
            await call.change_stream(chat_id, stream)
            await add_to_queue(chat_id, media=media_path, type=type_)
            return await aux.edit("✅ Streaming Started ...")
        else:
            position = await add_to_queue(chat_id, media=media_path, type=type_)
            return await aux.edit(f"✅ Added to Queue at position {position}")
    except Exception:
        stream = await get_media_stream(media_path, type_)
        await call.join_group_call(chat_id, stream, auto_start=False)
        await add_to_queue(chat_id, media=media_path, type=type_)
        return await aux.edit("✅ Streaming Started ...")
