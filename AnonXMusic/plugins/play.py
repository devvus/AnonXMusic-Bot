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

    # Dynamic User-Agent Rotation
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
    ]

    base_ydl_opts = {
        'outtmpl': f'{DOWNLOAD_DIR}/%(id)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'geo_bypass': True,
        'default_search': 'ytsearch',
        'user_agent': random.choice(USER_AGENTS),
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web', 'ios'],
                'skip': ['dash', 'hls']
            }
        }
    }
    
    if os.path.exists(COOKIES_FILE_PATH):
        base_ydl_opts['cookiefile'] = COOKIES_FILE_PATH

    try:
        loop = asyncio.get_event_loop()
        
        def dynamic_download(q):
            # Step 1: Detect available formats dynamically
            with YoutubeDL(base_ydl_opts) as ydl:
                try:
                    info = ydl.extract_info(q, download=False)
                    if 'entries' in info:
                        info = info['entries'][0]
                    
                    video_id = info['id']
                    formats = info.get('formats', [])
                    
                    # Step 2: Filter and rank formats
                    # Priority: Audio-only opus > Audio-only m4a > Best Audio > Any stream with audio
                    audio_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
                    
                    best_format = None
                    if audio_formats:
                        # Try to find opus/webm first for performance
                        opus = [f for f in audio_formats if f.get('ext') == 'webm' or 'opus' in f.get('acodec', '').lower()]
                        if opus:
                            best_format = opus[0]['format_id']
                        else:
                            best_format = audio_formats[0]['format_id']
                    
                    # Step 3: Download with chosen format or fallback
                    final_opts = base_ydl_opts.copy()
                    if best_format:
                        final_opts['format'] = f"{best_format}/bestaudio/best"
                    else:
                        final_opts['format'] = "bestaudio/best"
                        
                    with YoutubeDL(final_opts) as ydl_final:
                        return ydl_final.extract_info(video_id, download=True)
                        
                except Exception as e:
                    logger.warning(f"Dynamic detection failed: {e}. Falling back to aggressive mode.")
                    # Aggressive Fallback: Just get 'best' and let yt-dlp handle it
                    fallback_opts = base_ydl_opts.copy()
                    fallback_opts['format'] = "best"
                    with YoutubeDL(fallback_opts) as ydl_fb:
                        return ydl_fb.extract_info(q, download=True)

        info = await loop.run_in_executor(None, dynamic_download, query)
        
        if 'entries' in info:
            info = info['entries'][0]
            
        video_id = info['id']
        title = info['title']
        
        # Verify file existence (yt-dlp might change extension during merge/conversion)
        files = [f for f in os.listdir(DOWNLOAD_DIR) if f.startswith(video_id)]
        if not files:
            raise Exception("Download completed but file not found on disk.")
            
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
        logger.error(f"Final YouTube Error: {e}")
        await m.edit_text(
            f"❌ **YouTube Error:** `{str(e)[:100]}`\n\n"
            "**Troubleshooting:**\n"
            "1. Try a different song name.\n"
            "2. Ensure the bot is not blocked by YouTube.\n"
            "3. Update your cookies.txt if the problem persists. 🌸"
        )

def cleanup_downloads():
    if os.path.exists(DOWNLOAD_DIR):
        for f in os.listdir(DOWNLOAD_DIR):
            if f != ".gitkeep":
                try:
                    os.remove(os.path.join(DOWNLOAD_DIR, f))
                except: pass
