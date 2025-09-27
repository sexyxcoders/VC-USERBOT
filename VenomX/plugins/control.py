from VenomX.modules.clients import app, call
from VenomX.modules.helpers import cdz, eor
from VenomX.modules.queues import add_to_queue, get_from_queue, clear_queue, is_queue_empty, task_done
from VenomX.modules.streams import get_media_stream
from pyrogram import filters

# -------------------------------
# Pause stream
# -------------------------------
@app.on_message(cdz(["pause", "pse"]) & ~filters.private)
async def pause_stream(client, message):
    if message.sender_chat:
        return
    chat_id = message.chat.id
    try:
        call_obj = await call.get_call(chat_id)
        if call_obj.status == "playing":
            await call.pause_stream(chat_id)
            return await eor(message, "⏸ Stream Paused!")
        elif call_obj.status == "paused":
            return await eor(message, "⚠ Already Paused!")
        elif call_obj.status == "not_playing":
            return await eor(message, "❌ Nothing Streaming!")
    except Exception:
        return await eor(message, "❌ I am Not in VC!")

# -------------------------------
# Resume stream
# -------------------------------
@app.on_message(cdz(["resume", "rsm"]) & ~filters.private)
async def resume_stream(client, message):
    if message.sender_chat:
        return
    chat_id = message.chat.id
    try:
        call_obj = await call.get_call(chat_id)
        if call_obj.status == "paused":
            await call.resume_stream(chat_id)
            return await eor(message, "▶ Stream Resumed!")
        elif call_obj.status == "playing":
            return await eor(message, "⚠ Already Playing!")
        elif call_obj.status == "not_playing":
            return await eor(message, "❌ Nothing Streaming!")
    except Exception:
        return await eor(message, "❌ I am Not in VC!")

# -------------------------------
# Skip stream
# -------------------------------
@app.on_message(cdz(["skip", "skp"]) & ~filters.private)
async def skip_stream(client, message):
    if message.sender_chat:
        return
    chat_id = message.chat.id
    try:
        call_obj = await call.get_call(chat_id)
        if call_obj.status in ["playing", "paused"]:
            await task_done(chat_id)
            queue_empty = await is_queue_empty(chat_id)
            if queue_empty:
                await call.leave_group_call(chat_id)
                return await eor(message, "❌ Queue empty, leaving VC...")
            
            # Get next in queue
            check = await get_from_queue(chat_id)
            media = check["media"]
            type_ = check["type"]
            stream = await get_media_stream(media, type_)
            await call.change_stream(chat_id, stream)
            return await eor(message, "▶ Now Streaming next in Queue ...")
        elif call_obj.status == "not_playing":
            return await eor(message, "❌ Nothing Playing!")
    except Exception:
        return await eor(message, "❌ I am Not in VC!")

# -------------------------------
# Stop stream
# -------------------------------
@app.on_message(cdz(["stop", "stp", "end"]) & ~filters.private)
async def stop_stream(client, message):
    if message.sender_chat:
        return
    chat_id = message.chat.id
    try:
        call_obj = await call.get_call(chat_id)
        if call_obj.status in ["playing", "paused", "not_playing"]:
            await clear_queue(chat_id)
            await call.leave_group_call(chat_id)
            return await eor(message, "⏹ Stream Ended!")
    except Exception:
        return await eor(message, "❌ I am Not in VC!")
