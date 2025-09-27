import asyncio
import pyrogram
import sys
import signal

from VenomX.modules.clients import app, bot, call
from VenomX.plugins import load_plugins

# Handle graceful shutdown on Heroku or Ctrl+C
def shutdown_handler(sig, frame):
    print("🛑 Received shutdown signal. Exiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)


async def main():
    print("🚀 Starting VenomX clients...")

    try:
        # Start Userbot
        await app.start()
        print("✅ User client started.")

        # Start Bot (optional)
        await bot.start()
        print("✅ Bot client started.")

        # Start PyTgCalls
        await call.start()
        print("✅ PyTgCalls client started.")

        # Load plugins
        await load_plugins()
        print("✅ All plugins loaded.")

        print("🎉 VenomX is now running!")
        await pyrogram.idle()  # Keep the app running

    except Exception as e:
        print(f"❌ Startup Error: {e}")

    finally:
        print("🛑 Shutting down VenomX...")
        await call.stop()
        await bot.stop()
        await app.stop()
        print("✅ VenomX stopped cleanly.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("🛑 Forced stop.")
        sys.exit(0)