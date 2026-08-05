from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    await message.reply_text("Hello! I am your cute anime music bot. I'm finally awake! How can I help you? ✨")

@Client.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    help_text = (
        "**Anime Music Bot Help** 🎵\n\n"
        "/play [song name or link] - Play music in voice chat\n"
        "/pause - Pause the current music\n"
        "/resume - Resume the paused music\n"
        "/skip - Skip to the next track\n"
        "/stop - Stop music and leave voice chat\n"
        "/ping - Check bot latency\n\n"
        "Enjoy the music! 🌸"
    )
    await message.reply_text(help_text)
