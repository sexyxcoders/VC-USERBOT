from pyrogram import Client
from pytgcalls import PyTgCalls
from VenomX import config

# -------------------------------
# Pyrogram User Client
# -------------------------------
app = Client(
    session_name="userbot",        # Changed from 'name' to 'session_name'
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    workdir="sessions",            # Optional: keep sessions in a folder
    parse_mode="html"              # Optional: make messages parse HTML
)

# -------------------------------
# Pyrogram Bot Client
# -------------------------------
bot = Client(
    session_name="bot",            # Changed from 'name' to 'session_name'
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    workdir="sessions",
    parse_mode="html"
)

# -------------------------------
# PyTgCalls Client
# -------------------------------
call = PyTgCalls(app)              # Attach PyTgCalls to the user client
