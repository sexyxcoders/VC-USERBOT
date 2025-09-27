from pyrogram import Client
from VenomX import config

# === Import PyTgCalls (handles both v2.x and v3.x) ===
try:
    # v3.x (latest dev6)
    from pytgcalls import PyTgCalls
except ImportError:
    # v2.x / old structure
    from pytgcalls.pytgcalls import PyTgCalls

# === USERBOT CLIENT ===
app = Client(
    "VenomXUser",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.STRING_SESSION
)

# === BOT CLIENT (for commands) ===
bot = Client(
    "VenomXBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

# === VC CLIENT ===
call = PyTgCalls(app)