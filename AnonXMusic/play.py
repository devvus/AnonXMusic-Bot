from pyrogram import Client, filters
from pyrogram.types import Message
from yt_dlp import YoutubeDL

# Queue for music playback
music_queue = []

@Client.on_message(filters.command("play"))
async def play_command(client: Client, message: Message):
    from AnonXMusic.__main__ import call_py
    
    if len(message.command) < 2:
        await message.reply_text("Please provide a song name or link!")
        return

    query = " ".join(message.command[1:])
    m = await message.reply_text(f"Searching for `{query}`... 🔍")

    try:
        ydl_opts = {
            'format': 'bestaudio',
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch',
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            audio_url = info['url']
            title = info['title']

        music_queue.append({'title': title, 'url': audio_url})
        if len(music_queue) == 1:
            await start_playback(chat_id=message.chat.id, audio_url=audio_url)
            await m.edit_text(f"Now playing: **{title}** 🎶")
        else:
            await m.edit_text(f"Added to queue: **{title}** at position #{len(music_queue)-1}")

    except Exception as e:
        await m.edit_text(f"Error: {e}")

async def start_playback(chat_id: int, audio_url: str):
    from AnonXMusic.__main__ import call_py
    from pytgcalls.types import AudioPiped
    try:
        await call_py.join_group_call(chat_id, AudioPiped(audio_url))
    except Exception as e:
        print(f"Playback error: {e}")

async def play_next_track(chat_id: int):
    if music_queue:
        music_queue.pop(0)
        if music_queue:
            next_track = music_queue[0]
            await start_playback(chat_id, next_track['url'])
