from typing import Union, List
from pyrogram import filters
from pyrogram.types import Message
from pytgcalls import StreamEnd
from VenomX.modules.clients import app, call
from VenomX.modules.streams import get_media_stream
from VenomX.modules import queues
from VenomX import config

# Command filters
def cdx(commands: Union[str, List[str]]):
    return filters.command(commands, config.COMMAND_PREFIXES)

def cdz(commands: Union[str, List[str]]):
    return filters.command(commands, config.COMMAND_HANDLERS)

# Edit or reply
async def eor(message: Message, *args, **kwargs):
    msg = message.edit_text if getattr(message, "outgoing", False) else (message.reply_to_message or message).reply_text
    return await msg(*args, **kwargs)

# Stream-end handler
async def call_decorators():
    @call.on_stream_end()
    async def stream_end_handler(update: StreamEnd):
        chat_id = update.chat_id
        await queues.task_done(chat_id)
        if await queues.is_queue_empty(chat_id):
            try:
                await call.leave_group_call(chat_id)
            except:
                return
        else:
            check = await queues.get_from_queue(chat_id)
            stream = await get_media_stream(check["media"], check["type"])
            await call.change_stream(chat_id, stream)
            await app.send_message(chat_id, "🎵 Now Streaming ...")
