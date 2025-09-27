from pyrogram import Client
from VenomX import config

# Try importing PyTgCalls in a version-agnostic way
try:
    from pytgcalls import PyTgCalls
except ImportError:
    from pytgcalls.pytgcalls import PyTgCalls

# Userbot client
app = Client(
    "VenomX",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.STRING_SESSION
)

# Bot client (optional)
bot = Client(
    "VenomXBot",
    bot_token=config.BOT_TOKEN,
    api_id=config.API_ID,
    api_hash=config.API_HASH
)

# PyTgCalls client
call = PyTgCalls(app)
