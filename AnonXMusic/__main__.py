import asyncio
import os
import time
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, STRING_SESSION, BOT_TOKEN, OWNER_ID, LOG_GROUP_ID, LOG_CHAT_ID, MONGO_DB_URI

# Optional PyTgCalls for sandbox testing
try:
    from pytgcalls import PyTgCalls
    HAS_PYTGCALLS = True
except ImportError:
    HAS_PYTGCALLS = False
    print("PyTgCalls not found. Music features will be disabled (Sandbox Mode).")

# Initialize Bot Client (The Interface)
app = Client(
    "AnonXBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# Initialize Assistant Client (The Streamer)
userbot = Client(
    "AnonXAssistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION,
)

if HAS_PYTGCALLS:
    call_py = PyTgCalls(userbot)
else:
    call_py = None

# Import handlers AFTER app is defined
# Note: Handlers should now be registered on 'app'
from AnonXMusic import start, play, controls

async def main():
    print("Starting bot and assistant...")
    try:
        await app.start()
        print("Bot Client started!")
        
        await userbot.start()
        print("Assistant Client started!")
        
        if HAS_PYTGCALLS and call_py:
            await call_py.start()
            print("PyTgCalls Client started!")
        else:
            print("Skipping PyTgCalls startup.")

        # Send startup message to log group
        try:
            await app.send_message(LOG_GROUP_ID, "Bot and Assistant are online!")
        except Exception as e:
            print(f"Failed to send startup message: {e}")

        print("Bot is fully online!")
        await asyncio.Event().wait()
        
    except Exception as e:
        print(f"Critical error during startup: {e}")

@app.on_message(filters.command("ping"))
async def ping_command(client: Client, message: Message):
    start_time = time.time()
    msg = await message.reply_text("Pinging...")
    end_time = time.time()
    latency = round((end_time - start_time) * 1000, 2)
    await msg.edit_text(f"Pong! Latency: {latency}ms")

if __name__ == "__main__":
    asyncio.run(main())
