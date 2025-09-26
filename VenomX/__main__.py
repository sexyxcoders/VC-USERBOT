import asyncio
import pyrogram

from VenomX import app, bot, call
from VenomX.plugins import load_plugins
from VenomX.modules.events import call_decorators


loop = asyncio.get_event_loop()


async def init():
    print("Starting all clients ...")
    try:
        # Start Pyrogram user client
        await app.start()
        print("User client started.")

        # Start Pyrogram bot client
        await bot.start()
        print("Bot client started.")

        # Start PyTgCalls client
        await call.start()
        print("PyTgCalls client started.")

        # Register stream end handlers (updated for v2.2)
        await call_decorators()
        print("Stream handlers registered.")

        # Load plugins
        await load_plugins()
        print("All plugins loaded.")
        
    except Exception as e:
        print(f"Error during startup: {e}")
        return

    print("Userbot Now Started !!")
    await pyrogram.idle()


if __name__ == "__main__":
    loop.run_until_complete(init())
    print("Userbot is Now Stopped !!")
