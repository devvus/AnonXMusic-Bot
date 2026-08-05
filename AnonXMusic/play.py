from pyrogram import Client, filters
from pyrogram.types import Message
from AnonXMusic.__main__ import app
from pytgcalls import StreamType
from pytgcalls.types import AudioPiped, AudioVideoPiped
from youtube_dlp import YoutubeDL
from AnonXMusic.__main__ import call_py

# Queue for music playback
music_queue = []

@app.on_message(filters.command("play"))
async def play_command(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a song name or link to play.")
        return

    query = " ".join(message.command[1:])
    await message.reply_text(f"Searching for {query}...")

    try:
        with YoutubeDL({'format': 'bestaudio', 'noplaylist': True}) as ydl:
            info = ydl.extract_info(query, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            audio_url = info['url']
            title = info['title']

        # Add to queue and play
        music_queue.append({'title': title, 'url': audio_url})
        if len(music_queue) == 1:
            await start_playback(client, message.chat.id, audio_url)
            await message.reply_text(f"Now playing: {title}")
        else:
            await message.reply_text(f"Added to queue: {title}. Position: {len(music_queue) - 1}")

    except Exception as e:
        await message.reply_text(f"Error playing music: {e}")

async def start_playback(client: Client, chat_id: int, audio_url: str):
    try:
        await call_py.join_group_call(
            chat_id,
            AudioPiped(audio_url),
            stream_type=StreamType().pulse_stream
        )
    except Exception as e:
        print(f"Error joining group call: {e}")
        # Handle cases where bot is not in VC or other errors

async def play_next_track(client: Client, chat_id: int):
    if music_queue:
        music_queue.pop(0) # Remove current track
        if music_queue:
            next_track = music_queue[0]
            await start_playback(client, chat_id, next_track['url'])
            await client.send_message(chat_id, f"Now playing next: {next_track['title']}")
        else:
            await client.send_message(chat_id, "Queue is empty. Leaving voice chat.")
            await call_py.leave_group_call(chat_id)

