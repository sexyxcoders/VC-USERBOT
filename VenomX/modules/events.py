from typing import Union, List
from pyrogram import filters
from pyrogram.types import Message

from VenomX import config
from VenomX.modules import queues
from VenomX.modules.clients import app, call
from VenomX.modules.streams import get_media_stream
from pytgcalls.types import StreamEnded  # v2 event


# Command filters
def cdx(commands: Union[str, List[str]]):
    return filters.command(commands, config.COMMAND_PREFIXES)


def cdz(commands: Union[str, List[str]]):
    return filters.command(commands, config.COMMAND_HANDLERS)


# Edit or reply message helper
async def eor(message: Message, *args, **kwargs) -> Message:
    try:
        msg = (
            message.edit_text
            if bool(message.from_user and message.from_user.is_self or message.outgoing)
            else (message.reply_to_message or message).reply_text
        )
    except:
        msg = (
            message.edit_text
            if bool(message.from_user and message.outgoing)
            else (message.reply_to_message or message).reply_text
        )

    return await msg(*args, **kwargs)


# Call-related decorators and event handlers
async def call_decorators():
    # Handler to leave group call if queue is empty
    async def stream_services_handler(client, chat_id: int):
        queue_empty = await queues.is_queue_empty(chat_id)
        if not queue_empty:
            await queues.clear_queue(chat_id)
        try:
            return await call.leave_group_call(chat_id)
        except:
            return

    # Stream end handler for PyTgCalls v2.2+
    async def stream_end_handler(update: StreamEnded):
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
            type = check["type"]
            stream = await get_media_stream(media, type)
            await call.change_stream(chat_id, stream)
            await app.send_message(chat_id, "Streaming ...")

    # Attach handler to PyTgCalls client
    call.add_stream_handler(stream_end_handler)
