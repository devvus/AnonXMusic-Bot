import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from AnonXMusic import start, play, controls # Import command handlers
import time # For ping command
from config import API_ID, API_HASH, STRING_SESSION, OWNER_ID, LOG_GROUP_ID, LOG_CHAT_ID, MONGO_DB_URI

# Initialize Pyrogram Client
app = Client(
    "AnonXMusic", # Session name

    api_id=API_ID,
    api_hash=API_HASH,
    session_name=STRING_SESSION,
)

# Initialize PyTgCalls Client
call_py = PyTgCalls(app)

async def main():
    print("Starting bot...")
    await app.start()
    await call_py.start()
    print("Bot started!")

    # Send startup message to log group
    try:
        await app.send_message(LOG_GROUP_ID, "Bot started successfully!")
    except Exception as e:
        print(f"Failed to send startup message to log group: {e}")

    # Keep the bot running
    await asyncio.Event().wait()

@app.on_message(filters.command("ping"))
async def ping_command(client: Client, message: Message):
    start_time = time.time()
    await message.reply_text("Pinging...")
    end_time = time.time()
    latency = round((end_time - start_time) * 1000, 2)
    await message.edit_text(f"Pong! Latency: {latency}ms")


if __name__ == "__main__":
    asyncio.run(main())

