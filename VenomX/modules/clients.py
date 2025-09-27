from pyrogram import Client
from VenomX import config

# PyTgCalls v2.x
from py_tgcalls import PyTgCalls

# === USERBOT CLIENT ===
app = Client(
    "VenomXUser",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.STRING_SESSION  # Must be set in Heroku config
)

# === BOT CLIENT (for commands) ===
bot = Client(
    "VenomXBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN  # Optional if you have a bot
)

# === VOICE CHAT CLIENT ===
call = PyTgCalls(app)

# Optional: simple print logs to confirm initialization
print("✅ Clients initialized: Userbot, Bot, PyTgCalls")