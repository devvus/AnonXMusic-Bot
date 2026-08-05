import asyncio
import logging
from pyrogram import Client, idle
from config import API_ID, API_HASH, STRING_SESSION, BOT_TOKEN, OWNER_ID

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(name)s: %(message)s")
logger = logging.getLogger("AnonXMusic")

# Optional PyTgCalls
try:
    from pytgcalls import PyTgCalls
    HAS_PYTGCALLS = True
except ImportError:
    HAS_PYTGCALLS = False
    logger.info("PyTgCalls not found.")

# Initialize Clients with in_memory=True to avoid session file conflicts
app = Client(
    "AnonXBotFinal",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="AnonXMusic"),
    in_memory=True
)

userbot = Client(
    "AnonXAssistantFinal",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION,
    in_memory=True
)

if HAS_PYTGCALLS:
    call_py = PyTgCalls(userbot)
else:
    call_py = None

async def main():
    logger.info("Starting bot and assistant...")
    try:
        await app.start()
        logger.info("Bot Client started!")
        
        await userbot.start()
        logger.info("Assistant Client started!")
        
        if HAS_PYTGCALLS and call_py:
            await call_py.start()
            logger.info("PyTgCalls Client started!")

        # Send startup message
        try:
            await app.send_message(OWNER_ID, "🚀 Bot is online and ready on Railway!")
        except Exception as e:
            logger.warning(f"Failed to send startup message to owner: {e}")

        logger.info("Bot is fully online!")
        await idle()
        
    except Exception as e:
        logger.error(f"Critical error during startup: {e}", exc_info=True)
    finally:
        # Graceful shutdown
        if app.is_connected:
            await app.stop()
        if userbot.is_connected:
            await userbot.stop()

if __name__ == "__main__":
    # Use the same loop for everything
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
