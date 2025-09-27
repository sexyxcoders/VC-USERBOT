from pyrogram import Client
from VenomX import config

# Correct import for py-tgcalls v2.1.0
from pytgcalls import PyTgCalls

# === USERBOT CLIENT ===
app = Client(
    "VenomXUser",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.STRING_SESSION
)

# === BOT CLIENT ===
bot = Client(
    "VenomXBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

# === VOICE CHAT CLIENT ===
call = PyTgCalls(app)

print("✅ Clients initialized: Userbot, Bot, PyTgCalls")