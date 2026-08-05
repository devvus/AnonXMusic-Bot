import os
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from yt_dlp import YoutubeDL
from pytgcalls.types import MediaStream
from config import COOKIES_FILE_PATH

logger = logging.getLogger("AnonXMusic.play")
music_queue = []

async def play_command(client: Client, message: Message):
    # Dynamic import to avoid circular dependency
    from AnonXMusic.__main__ import call_py
    
    if len(message.command) < 2:
        await message.reply_text("❌ **Please provide a song name or link!**")
        return

    query = " ".join(message.command[1:])
    m = await message.reply_text(f"🔍 **Searching for** `{query}`... ✨")

    # The most robust YTDL options possible
    ydl_opts = {
        'format': "bestaudio/best",
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'geo_bypass': True,
        'default_search': 'ytsearch',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }
    
    if os.path.exists(COOKIES_FILE_PATH):
        ydl_opts['cookiefile'] = COOKIES_FILE_PATH

    try:
        loop = asyncio.get_event_loop()
        
        def extract_info(q):
            # We try multiple formats in sequence if the first one fails
            formats_to_try = ["bestaudio/best", "bestaudio", "best", "ba/b"]
            last_error = None
            
            for fmt in formats_to_try:
                try:
                    current_opts = ydl_opts.copy()
                    current_opts['format'] = fmt
                    with YoutubeDL(current_opts) as ydl:
                        return ydl.extract_info(q, download=False)
                except Exception as e:
                    last_error = e
                    logger.warning(f"Format {fmt} failed: {e}")
                    continue
            
            raise last_error

        info = await loop.run_in_executor(None, extract_info, query)
        
        if 'entries' in info:
            info = info['entries'][0]
        
        audio_url = info['url']
        title = info['title']

        music_queue.append({'title': title, 'url': audio_url, 'chat_id': message.chat.id})
        
        if len(music_queue) == 1:
            try:
                # Use MediaStream for PyTgCalls v2
                await call_py.join_group_call(message.chat.id, MediaStream(audio_url))
                await m.edit_text(f"🎶 **Now playing:** **{title}** ✨")
            except Exception as e:
                logger.error(f"Playback Error: {e}")
                await m.edit_text(f"❌ **Playback Error:** `{e}`")
                music_queue.pop(0)
        else:
            await m.edit_text(f"🎼 **Added to queue:** **{title}** at position #{len(music_queue)-1} 🌸")

    except Exception as e:
        logger.error(f"Final Error: {e}")
        error_msg = str(e)
        if "Requested format is not available" in error_msg:
            await m.edit_text("❌ **YouTube Error:** The requested audio format is not available for this video. Try another song! 🌸")
        else:
            await m.edit_text(f"❌ **YouTube Error:** `{error_msg[:100]}`\n\nTry a different search term! 🌸")
