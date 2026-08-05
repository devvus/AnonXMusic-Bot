import os
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from yt_dlp import YoutubeDL
from pytgcalls.types import MediaStream
from config import COOKIES_FILE_PATH

logger = logging.getLogger("AnonXMusic.play")

# Queue storage (In-memory for this refactor)
music_queue = []

async def play_command(client: Client, message: Message):
    from AnonXMusic.__main__ import call_py
    
    if len(message.command) < 2:
        await message.reply_text("❌ **Please provide a song name or link!**")
        return

    query = " ".join(message.command[1:])
    m = await message.reply_text(f"🔍 **Searching for** `{query}`... ✨")

    # Robust YTDL Options
    ydl_opts = {
        'format': "bestaudio[ext=m4a]/bestaudio/best", # Primary Format
        'noplaylist': True,
        'quiet': True,
        'nocheckcertificate': True,
        'geo_bypass': True,
        'extract_flat': False,
        'default_search': 'ytsearch',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }
    
    # Load cookies if present
    if os.path.exists(COOKIES_FILE_PATH):
        ydl_opts['cookiefile'] = COOKIES_FILE_PATH
        logger.info(f"Using cookies from {COOKIES_FILE_PATH}")

    try:
        loop = asyncio.get_event_loop()
        
        def extract_info(q, opts):
            with YoutubeDL(opts) as ydl:
                try:
                    return ydl.extract_info(q, download=False)
                except Exception as e:
                    logger.warning(f"Extraction failed with primary format: {e}. Trying fallback...")
                    opts['format'] = "ba/b" # Fallback 1
                    try:
                        return ydl.extract_info(q, download=False)
                    except Exception:
                        logger.warning("Fallback 1 failed. Trying ultimate fallback...")
                        opts['format'] = "best" # Ultimate Fallback
                        return ydl.extract_info(q, download=False)

        info = await loop.run_in_executor(None, extract_info, query, ydl_opts)
        
        if 'entries' in info:
            info = info['entries'][0]
        
        audio_url = info['url']
        title = info['title']

        # Add to queue
        music_queue.append({'title': title, 'url': audio_url, 'chat_id': message.chat.id})
        
        if len(music_queue) == 1:
            try:
                # Use MediaStream for PyTgCalls v2
                await call_py.join_group_call(
                    message.chat.id, 
                    MediaStream(audio_url)
                )
                await m.edit_text(f"🎶 **Now playing:** **{title}** ✨")
            except Exception as e:
                logger.error(f"Playback Error: {e}")
                await m.edit_text(f"❌ **Playback Error:** `{e}`")
                music_queue.pop(0)
        else:
            await m.edit_text(f"🎼 **Added to queue:** **{title}** at position #{len(music_queue)-1} 🌸")

    except Exception as e:
        logger.error(f"Extraction Error: {e}")
        await m.edit_text(f"❌ **Extraction Error:** `{str(e)[:150]}`")

async def start_playback(chat_id: int, audio_url: str):
    from AnonXMusic.__main__ import call_py
    try:
        await call_py.join_group_call(chat_id, MediaStream(audio_url))
    except Exception as e:
        logger.error(f"Background Playback Error: {e}")
