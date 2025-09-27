import asyncio
import pyrogram

from VenomX import app, bot, call
from VenomX.plugins import load_plugins
from VenomX.modules.events import call_decorators

loop = asyncio.get_event_loop()

async def init():
    print("🔹 Starting all clients ...")

    try:
        # Start Pyrogram user client
        await app.start()
        print("✅ User client started.")

        # Start Pyrogram bot client
        await bot.start()
        print("✅ Bot client started.")

        # Start PyTgCalls client
        await call.start()
        print("✅ PyTgCalls client started.")

        # Register stream end handlers (0.9.7 style)
        await call_decorators()
        print("✅ Stream handlers registered.")

        # Load plugins
        await load_plugins()
        print("✅ All plugins loaded.")

    except Exception as e:
        print(f"❌ Error during startup: {e}")
        return

    print("🎵 Userbot Now Started !!")
    # Keep running until manually stopped
    await pyrogram.idle()

if __name__ == "__main__":
    try:
        loop.run_until_complete(init())
    except (KeyboardInterrupt, SystemExit):
        print("\n⚡ Userbot is Now Stopped !!")
