from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("pause"))
async def pause_command(client: Client, message: Message):
    from AnonXMusic.__main__ import call_py, HAS_PYTGCALLS
    if not HAS_PYTGCALLS: return await message.reply_text("Disabled in Sandbox.")
    try:
        await call_py.pause_stream(message.chat.id)
        await message.reply_text("Paused ⏸️")
    except Exception as e:
        await message.reply_text(f"Error: {e}")

@Client.on_message(filters.command("resume"))
async def resume_command(client: Client, message: Message):
    from AnonXMusic.__main__ import call_py, HAS_PYTGCALLS
    if not HAS_PYTGCALLS: return await message.reply_text("Disabled in Sandbox.")
    try:
        await call_py.resume_stream(message.chat.id)
        await message.reply_text("Resumed ▶️")
    except Exception as e:
        await message.reply_text(f"Error: {e}")

@Client.on_message(filters.command("skip"))
async def skip_command(client: Client, message: Message):
    from AnonXMusic.__main__ import call_py, HAS_PYTGCALLS
    from AnonXMusic.play import music_queue, play_next_track
    if not HAS_PYTGCALLS: return await message.reply_text("Disabled in Sandbox.")
    if not music_queue: return await message.reply_text("Queue is empty.")
    await play_next_track(message.chat.id)
    await message.reply_text("Skipped ⏭️")

@Client.on_message(filters.command(["stop", "end"]))
async def stop_command(client: Client, message: Message):
    from AnonXMusic.__main__ import call_py, HAS_PYTGCALLS
    from AnonXMusic.play import music_queue
    if not HAS_PYTGCALLS: return await message.reply_text("Disabled in Sandbox.")
    music_queue.clear()
    try:
        await call_py.leave_group_call(message.chat.id)
        await message.reply_text("Stopped and left VC 👋")
    except Exception as e:
        await message.reply_text(f"Error: {e}")
