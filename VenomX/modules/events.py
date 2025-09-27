from typing import Union, List
from pyrogram import filters
from pyrogram.types import Message
from VenomX import config
from VenomX.modules import queues
from VenomX.modules.clients import app, call
from VenomX.modules.streams import get_media_stream
from pytgcalls import StreamEnd

# Command filters
def cdx(commands: Union[str, List[str]]):
    return filters.command(commands, config.COMMAND_PREFIXES)

def cdz(commands: Union[str, List[str]]):
    return filters.command(commands, config.COMMAND_HANDLERS)

# Edit or reply helper
async def eor(message: Message, *args, **kwargs) -> Message:
    msg = message.edit_text if getattr(message.from_user, "is_self", False) or getattr(message, "outgoing", False) else (message.reply_to_message or message).reply_text
    return await msg(*args, **kwargs)

# Stream end handler registration
async def call_decorators():
    @call.on_stream_end()
    async def stream_end_handler(update: StreamEnd):
        chat_id = update.chat_id
        await queues.task_done(chat_id)
        queue_empty = await queues.is_queue_empty(chat_id)
        if queue_empty:
            try:
                await call.leave_group_call(chat_id)
            except:
                return
        else:
            check = await queues.get_from_queue(chat_id)
            media = check["media"]
            type_ = check["type"]
            stream = await get_media_stream(media, type_)
            await call.change_stream(chat_id, stream)
            await app.send_message(chat_id, "🎵 Now Streaming ...")
