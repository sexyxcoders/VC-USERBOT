import asyncio
from pyrogram import idle
from VenomX import app, bot, call
from VenomX.plugins import load_plugins
from VenomX.modules.events import call_decorators

loop = asyncio.get_event_loop()

async def init():
    print("🔹 Starting clients...")
    await app.start()
    print("✅ User client started")
    await bot.start()
    print("✅ Bot client started")
    await call.start()
    print("✅ PyTgCalls client started")
    await call_decorators()
    print("✅ Stream handlers registered")
    await load_plugins()
    print("✅ All plugins loaded")
    print("🎵 Userbot Started")
    await idle()

if __name__ == "__main__":
    try:
        loop.run_until_complete(init())
    except (KeyboardInterrupt, SystemExit):
        print("⚡ Userbot stopped")
