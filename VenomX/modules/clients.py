from pyrogram import Client
from pytgcalls import GroupCallFactory
from VenomX import config

# Pyrogram client
app = Client(
    "VenomXUser",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.STRING_SESSION  # or leave out for .session file
)

bot = Client(
    "VenomXBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

# PyTgCalls initialization
call_factory = GroupCallFactory(app, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)
call = call_factory.get_group_call()
