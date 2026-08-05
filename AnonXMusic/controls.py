from pyrogram import Client, filters
from pyrogram.types import Message
from AnonXMusic.__main__ import app
from AnonXMusic.__main__ import call_py
from AnonXMusic.play import music_queue, play_next_track

@app.on_message(filters.command("pause"))
async def pause_command(client: Client, message: Message):
    try:
        await call_py.pause_stream(message.chat.id)
        await message.reply_text("Music paused! ⏸️")
    except Exception as e:
        await message.reply_text(f"Error pausing music: {e}")

@app.on_message(filters.command("resume"))
async def resume_command(client: Client, message: Message):
    try:
        await call_py.resume_stream(message.chat.id)
        await message.reply_text("Music resumed! ▶️")
    except Exception as e:
        await message.reply_text(f"Error resuming music: {e}")

@app.on_message(filters.command("skip"))
async def skip_command(client: Client, message: Message):
    try:
        if music_queue:
            await message.reply_text("Skipping to the next track... ⏭️")
            await play_next_track(client, message.chat.id)
        else:
            await message.reply_text("No more tracks in the queue to skip.")
    except Exception as e:
        await message.reply_text(f"Error skipping music: {e}")

@app.on_message(filters.command(["end", "stop"]))
async def end_command(client: Client, message: Message):
    try:
        music_queue.clear()
        await call_py.leave_group_call(message.chat.id)
        await message.reply_text("Music stopped and left voice chat! 👋")
    except Exception as e:
        await message.reply_text(f"Error stopping music: {e}")
