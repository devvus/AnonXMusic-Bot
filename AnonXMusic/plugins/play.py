import os
import asyncio
import logging
import shutil
from pyrogram import Client, filters
from pyrogram.types import Message
from yt_dlp import YoutubeDL
from pytgcalls.types import MediaStream
from config import COOKIES_FILE_PATH

logger = logging.getLogger("AnonXMusic.play")
music_queue = []

# Ensure downloads directory exists
DOWNLOAD_DIR = "downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

async def play_command(client: Client, message: Message):
    from AnonXMusic.__main__ import call_py
    
    if len(message.command) < 2:
        await message.reply_text("❌ **Please provide a song name or link!**")
        return

    query = " ".join(message.command[1:])
    m = await message.reply_text(f"🔍 **Searching for** `{query}`... ✨")

    # Robust YTDL Options for Downloading
    ydl_opts = {
        'format': "bestaudio[ext=webm][acodec=opus]/bestaudio/best",
        'outtmpl': f'{DOWNLOAD_DIR}/%(id)s.%(ext)s',
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
        
        def download_info(q):
            with YoutubeDL(ydl_opts) as ydl:
                try:
                    # First extract info
                    info = ydl.extract_info(q, download=True)
                    if 'entries' in info:
                        info = info['entries'][0]
                    return info
                except Exception as e:
                    logger.error(f"DETAILED YTDL ERROR: {e}")
                    # Debug: Try to list formats to see what is available from this IP
                    try:
                        with YoutubeDL({'quiet': True, 'cookiefile': COOKIES_FILE_PATH if os.path.exists(COOKIES_FILE_PATH) else None}) as ydl_debug:
                            debug_info = ydl_debug.extract_info(q, download=False)
                            formats = debug_info.get('formats', [])
                            format_ids = [f.get('format_id') for f in formats]
                            logger.info(f"AVAILABLE FORMATS FOR {q}: {format_ids}")
                    except Exception as de:
                        logger.error(f"COULD NOT EVEN LIST FORMATS: {de}")
                    
                    logger.warning(f"Download failed: {e}. Trying fallback to 'best'...")
                    ydl.params['format'] = "best"
                    info = ydl.extract_info(q, download=True)
                    if 'entries' in info:
                        info = info['entries'][0]
                    return info

        info = await loop.run_in_executor(None, download_info, query)
        
        video_id = info['id']
        ext = info['ext']
        file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.{ext}")
        title = info['title']

        music_queue.append({'title': title, 'file_path': file_path, 'chat_id': message.chat.id})
        
        if len(music_queue) == 1:
            try:
                # Use local file path for MediaStream
                await call_py.join_group_call(
                    message.chat.id, 
                    MediaStream(file_path)
                )
                await m.edit_text(f"🎶 **Now playing:** **{title}** ✨")
            except Exception as e:
                logger.error(f"Playback Error: {e}")
                await m.edit_text(f"❌ **Playback Error:** `{e}`")
                if os.path.exists(file_path):
                    os.remove(file_path)
                music_queue.pop(0)
        else:
            await m.edit_text(f"🎼 **Added to queue:** **{title}** at position #{len(music_queue)-1} 🌸")

    except Exception as e:
        logger.error(f"Final Error: {e}")
        await m.edit_text(f"❌ **YouTube Error:** `{str(e)[:100]}`\n\nTry a different search term! 🌸")

# Cleanup function to be called periodically or on exit
def cleanup_downloads():
    if os.path.exists(DOWNLOAD_DIR):
        shutil.rmtree(DOWNLOAD_DIR)
        os.makedirs(DOWNLOAD_DIR)
