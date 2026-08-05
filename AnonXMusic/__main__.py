import asyncio
import logging
from pyrogram import Client, idle, filters
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
    plugins=dict(root="AnonXMusic/plugins"),
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

# Direct command in main for testing
@app.on_message(filters.command("ping"))
async def ping_test(client, message):
    await message.reply_text("🏓 Pong! Bot is working directly from main!")

# Global logger to see if ANY message is received
@app.on_message(group=-1)
async def log_all_messages(client, message):
    logger.info(f"DEBUG: Received message from {message.from_user.id if message.from_user else 'Unknown'}: {message.text}")

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
            await app.send_message(OWNER_ID, "🚀 Bot is online with Telethon Assistant on Railway! (Plugin Fix)")
        except Exception as e:
            logger.error(f"Could not send startup message: {e}")

        logger.info("Bot is fully online!")
        
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
