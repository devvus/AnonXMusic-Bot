from pyrogram import Client, filters
from pyrogram.types import Message
from AnonXMusic.__main__ import app

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    await message.reply_text("Hello! I am a cute anime music bot. How can I help you today?")

@app.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    help_text = (
        "Here are the commands I understand:\n"
        "/play [song name or link] - Play music in voice chat\n"
        "/pause - Pause the current music\n"
        "/resume - Resume the paused music\n"
        "/skip - Skip to the next track\n"
        "/end or /stop - Stop music and leave voice chat\n"
        "/ping - Check my latency\n"
        "/start - Get a welcome message\n"
        "/help - Show this help message\n"
        "Enjoy the music! 🎶"
    )
    await message.reply_text(help_text)
