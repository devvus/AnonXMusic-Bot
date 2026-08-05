import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls.types import MediaStream

logger = logging.getLogger("AnonXMusic.controls")

async def pause_command(client: Client, message: Message):
    from AnonXMusic.__main__ import call_py
    try:
        await call_py.pause_stream(message.chat.id)
        await message.reply_text("⏸ **Paused playback!** ✨")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** `{e}`")

async def resume_command(client: Client, message: Message):
    from AnonXMusic.__main__ import call_py
    try:
        await call_py.resume_stream(message.chat.id)
        await message.reply_text("▶️ **Resumed playback!** ✨")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** `{e}`")

async def stop_command(client: Client, message: Message):
    from AnonXMusic.__main__ import call_py
    from AnonXMusic.plugins.play import music_queue
    try:
        await call_py.leave_group_call(message.chat.id)
        # Cleanup files in queue
        for track in music_queue:
            if os.path.exists(track['file_path']):
                os.remove(track['file_path'])
        music_queue.clear()
        await message.reply_text("⏹ **Stopped playback and cleared queue!** ✨")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** `{e}`")

async def skip_command(client: Client, message: Message):
    from AnonXMusic.__main__ import call_py
    from AnonXMusic.plugins.play import music_queue
    
    if not music_queue:
        await message.reply_text("❌ **Queue is empty!**")
        return
        
    try:
        old_track = music_queue.pop(0)
        if os.path.exists(old_track['file_path']):
            os.remove(old_track['file_path'])
            
        if not music_queue:
            await call_py.leave_group_call(message.chat.id)
            await message.reply_text("⏹ **Skipped! No more songs in queue. Left VC.** ✨")
            return
            
        next_track = music_queue[0]
        await call_py.change_stream(
            message.chat.id,
            MediaStream(next_track['file_path'])
        )
        await message.reply_text(f"⏭ **Skipped! Now playing:** **{next_track['title']}** ✨")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** `{e}`")
