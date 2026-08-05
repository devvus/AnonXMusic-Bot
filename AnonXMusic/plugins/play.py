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

    # The most aggressive YTDL options possible to bypass blocks
    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_DIR}/%(id)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'geo_bypass': True,
        'default_search': 'ytsearch',
        # Use a specific user agent that looks like a mobile device
        'user_agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
        # Extractor args to bypass some YouTube restrictions
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
                'skip': ['dash', 'hls']
            }
        }
    }
    
    if os.path.exists(COOKIES_FILE_PATH):
        ydl_opts['cookiefile'] = COOKIES_FILE_PATH
        logger.info(f"Using cookies: {COOKIES_FILE_PATH}")

    try:
        loop = asyncio.get_event_loop()
        
        def download_info(q):
            # Try 1: Best Audio only (Fastest)
            try:
                opts = ydl_opts.copy()
                opts['format'] = "bestaudio/best"
                with YoutubeDL(opts) as ydl:
                    return ydl.extract_info(q, download=True)
            except Exception as e:
                logger.warning(f"Try 1 (bestaudio) failed: {e}. Trying Try 2...")
                
            # Try 2: Any best quality (More likely to succeed)
            try:
                opts = ydl_opts.copy()
                opts['format'] = "best"
                with YoutubeDL(opts) as ydl:
                    return ydl.extract_info(q, download=True)
            except Exception as e:
                logger.warning(f"Try 2 (best) failed: {e}. Trying Try 3 (No format restriction)...")
            
            # Try 3: No format restriction at all (Let yt-dlp decide)
            opts = ydl_opts.copy()
            if 'format' in opts: del opts['format']
            with YoutubeDL(opts) as ydl:
                return ydl.extract_info(q, download=True)

        info = await loop.run_in_executor(None, download_info, query)
        
        if 'entries' in info:
            info = info['entries'][0]
            
        video_id = info['id']
        ext = info['ext']
        file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.{ext}")
        title = info['title']

        # Verify if file actually exists
        if not os.path.exists(file_path):
            # Sometimes yt-dlp changes extension during merge
            files = [f for f in os.listdir(DOWNLOAD_DIR) if f.startswith(video_id)]
            if files:
                file_path = os.path.join(DOWNLOAD_DIR, files[0])
            else:
                raise Exception("Downloaded file not found on disk.")

        music_queue.append({'title': title, 'file_path': file_path, 'chat_id': message.chat.id})
        
        if len(music_queue) == 1:
            try:
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
        logger.error(f"Final Extraction Error: {e}")
        await m.edit_text(f"❌ **YouTube Error:** `{str(e)[:150]}`\n\nTry a different search term or check cookies! 🌸")

def cleanup_downloads():
    if os.path.exists(DOWNLOAD_DIR):
        for f in os.listdir(DOWNLOAD_DIR):
            if f != ".gitkeep":
                try:
                    os.remove(os.path.join(DOWNLOAD_DIR, f))
                except: pass
