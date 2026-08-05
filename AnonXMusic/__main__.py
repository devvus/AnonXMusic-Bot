import asyncio
import logging
from pyrogram import Client, idle
from telethon import TelegramClient
from telethon.sessions import StringSession
from pytgcalls import PyTgCalls
from config import API_ID, API_HASH, STRING_SESSION, BOT_TOKEN, OWNER_ID

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(name)s: %(message)s")
logger = logging.getLogger("AnonXMusic")

# Initialize Pyrogram Bot Client
app = Client(
    "AnonXBotFinal",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="AnonXMusic"),
    in_memory=True
)

# Initialize Telethon Assistant Client
userbot = TelegramClient(
    StringSession(STRING_SESSION),
    API_ID,
    API_HASH
)

# Initialize PyTgCalls with Telethon client
call_py = PyTgCalls(userbot)

async def main():
    logger.info("Starting bot and assistant (Telethon)...")
    try:
        # Start Pyrogram Bot
        await app.start()
        logger.info("Pyrogram Bot Client started!")
        
        # Start Telethon Assistant
        await userbot.start()
        logger.info("Telethon Assistant Client started!")
        
        # Start PyTgCalls
        await call_py.start()
        logger.info("PyTgCalls Client started!")

        # Send startup message
        try:
            await app.send_message(OWNER_ID, "🚀 Bot is online with Telethon Assistant on Railway!")
        except Exception as e:
            logger.warning(f"Failed to send startup message to owner: {e}")

        logger.info("Bot is fully online!")
        
        # We use Pyrogram's idle since it's the main interface
        await idle()
        
    except Exception as e:
        logger.error(f"Critical error during startup: {e}", exc_info=True)
    finally:
        # Graceful shutdown
        if app.is_connected:
            await app.stop()
        if userbot.is_connected():
            await userbot.disconnect()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
