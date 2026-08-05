import os
import asyncio
import logging
import shutil
import random
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

    # The most robust YTDL options to bypass YouTube blocks on Cloud IPs
    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_DIR}/%(id)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'geo_bypass': True,
        'default_search': 'ytsearch',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'extractor_args': {
            'youtube': {
                'player_client': ['android_vr', 'android', 'web', 'ios'],
                'skip': ['dash', 'hls']
            }
        },
        # Smart format selection: Try audio first, then anything that works
        'format': 'bestaudio/ba/best',
    }
    
    if os.path.exists(COOKIES_FILE_PATH):
        ydl_opts['cookiefile'] = COOKIES_FILE_PATH
        logger.info(f"Using cookies: {COOKIES_FILE_PATH}")

    try:
        loop = asyncio.get_event_loop()
        
        def download_song(q):
            # Attempt 1: Standard download with fallbacks
            try:
                with YoutubeDL(ydl_opts) as ydl:
                    return ydl.extract_info(q, download=True)
            except Exception as e:
                logger.warning(f"Attempt 1 failed: {e}. Trying Attempt 2 with zero format restrictions...")
                
            # Attempt 2: No format restriction at all (Let yt-dlp pick ANYTHING)
            try:
                opts_no_fmt = ydl_opts.copy()
                opts_no_fmt['format'] = None # Let yt-dlp decide its own best fallback
                with YoutubeDL(opts_no_fmt) as ydl_none:
                    return ydl_none.extract_info(q, download=True)
            except Exception as e:
                logger.error(f"Attempt 2 failed: {e}. Trying final Search fallback...")
                raise e

        info = await loop.run_in_executor(None, download_song, query)
        
        if 'entries' in info:
            info = info['entries'][0]
            
        video_id = info['id']
        title = info['title']
        
        # Check all possible extensions (mp4, webm, m4a, etc.)
        files = [f for f in os.listdir(DOWNLOAD_DIR) if f.startswith(video_id)]
        if not files:
            raise Exception("YouTube blocked the download or no valid format was found. Please check your cookies.txt or try another song.")
            
        file_path = os.path.join(DOWNLOAD_DIR, files[0])

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
        logger.error(f"Ultimate Extraction Error: {e}")
        error_msg = str(e)
        if "Sign in to confirm you're not a bot" in error_msg or "429" in error_msg:
            await m.edit_text("❌ **YouTube Error:** YouTube has blocked this request. Please update your `cookies.txt` file with a fresh session! 🌸")
        else:
            await m.edit_text(f"❌ **YouTube Error:** `{error_msg[:100]}`\n\nTry searching with a different name! 🌸")

def cleanup_downloads():
    if os.path.exists(DOWNLOAD_DIR):
        for f in os.listdir(DOWNLOAD_DIR):
            if f != ".gitkeep":
                try:
                    os.remove(os.path.join(DOWNLOAD_DIR, f))
                except: pass
