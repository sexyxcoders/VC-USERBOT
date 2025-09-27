import asyncio
import pyrogram
import signal
import sys

from VenomX.modules.clients import app, bot, call
from VenomX.plugins import load_plugins


async def init():
    print("🚀 Starting all clients ...")
    try:
        await app.start()
        print("✅ User client started.")

        await bot.start()
        print("✅ Bot client started.")

        await call.start()
        print("✅ PyTgCalls client started.")

        await load_plugins()
        print("✅ All plugins loaded.")

        print("🎉 VenomX Now Running!")
        await pyrogram.idle()

    except Exception as e:
        print(f"❌ Startup Error: {e}")

    finally:
        print("🛑 Shutting down ...")
        await call.stop()
        await bot.stop()
        await app.stop()
        print("✅ VenomX Stopped Cleanly!")


if __name__ == "__main__":
    try:
        asyncio.run(init())
    except (KeyboardInterrupt, SystemExit):
        sys.exit("🛑 Forced Stop")