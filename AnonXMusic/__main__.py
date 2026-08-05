import asyncio
import logging
import os
import sys
from pyrogram import Client, idle, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telethon import TelegramClient
from telethon.sessions import StringSession
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
from motor.motor_asyncio import AsyncIOMotorClient
from config import (
    API_ID, API_HASH, STRING_SESSION, BOT_TOKEN, OWNER_ID, 
    LOG_GROUP_ID, LOG_CHAT_ID, MONGO_DB_URI, 
    START_IMG_URL, SUPPORT_CHAT, SUPPORT_CHANNEL
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("AnonXMusic")

# --- MONGODB FALLBACK ---
db = None
async def init_db():
    global db
    if MONGO_DB_URI:
        try:
            client = AsyncIOMotorClient(MONGO_DB_URI)
            await asyncio.wait_for(client.admin.command('ping'), timeout=5.0)
            db = client.AnonXMusic
            logger.info("Successfully connected to MongoDB!")
        except Exception as e:
            logger.error(f"MongoDB failed: {e}. Using In-Memory.")

# --- CLIENTS ---
app = Client(
    "AnonXMusicBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True
)

userbot = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
call_py = PyTgCalls(userbot)

# --- UI ---
START_TEXT = (
    "Hey {mention},\n"
    "This is {bot_name} ! 🌸\n\n"
    "A music player bot with some awesome and useful features. 🎶\n\n"
    "Click on the help button for more info. ✨"
)

HELP_TEXT = (
    "Click the buttons below to get information about my commands. 🎀\n\n"
    "Note: All commands can be used with / 📌"
)

def get_start_buttons(bot_username):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Add me to your group ➕", url=f"https://t.me/{bot_username}?startgroup=true")],
        [InlineKeyboardButton("Help 📜", callback_data="help_menu")],
        [
            InlineKeyboardButton("Support ↗️", url=SUPPORT_CHAT),
            InlineKeyboardButton("Channel ↗️", url=SUPPORT_CHANNEL)
        ]
    ])

def get_help_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👑 Admins", callback_data="h_admins"),
            InlineKeyboardButton("🔐 Auth", callback_data="h_auth"),
            InlineKeyboardButton("🚫 Blacklist", callback_data="h_blacklist")
        ],
        [
            InlineKeyboardButton("🌐 Language", callback_data="h_lang"),
            InlineKeyboardButton("🏓 Ping", callback_data="h_ping"),
            InlineKeyboardButton("🎵 Play", callback_data="h_play")
        ],
        [
            InlineKeyboardButton("🎼 Queue", callback_data="h_queue"),
            InlineKeyboardButton("📊 Stats", callback_data="h_stats"),
            InlineKeyboardButton("⚡ Sudoers", callback_data="h_sudo")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ])

# --- COMMANDS ---

@app.on_message(filters.command(["start", "start@Mdcikbot"]))
async def start_handler(client, message):
    bot = await client.get_me()
    mention = message.from_user.mention if message.from_user else "User"
    buttons = get_start_buttons(bot.username)
    
    try:
        if START_IMG_URL:
            await message.reply_photo(photo=START_IMG_URL, caption=START_TEXT.format(mention=mention, bot_name=bot.first_name), reply_markup=buttons)
        else:
            await message.reply_text(text=START_TEXT.format(mention=mention, bot_name=bot.first_name), reply_markup=buttons)
    except Exception as e:
        logger.error(f"Start Error: {e}")
        await message.reply_text(text=START_TEXT.format(mention=mention, bot_name=bot.first_name), reply_markup=buttons)

@app.on_message(filters.command(["help", "help@Mdcikbot"]))
async def help_handler(client, message):
    buttons = get_help_buttons()
    try:
        if START_IMG_URL:
            await message.reply_photo(photo=START_IMG_URL, caption=HELP_TEXT, reply_markup=buttons)
        else:
            await message.reply_text(text=HELP_TEXT, reply_markup=buttons)
    except Exception as e:
        logger.error(f"Help Error: {e}")
        await message.reply_text(text=HELP_TEXT, reply_markup=buttons)

@app.on_message(filters.command(["ping", "ping@Mdcikbot"]))
async def ping_handler(client, message):
    await message.reply_text("🏓 **Pong! Bot is active and healthy!** ✨")

# --- CALLBACKS ---

@app.on_callback_query(filters.regex("help_menu"))
async def help_menu_cb(client, query):
    await query.message.edit_caption(caption=HELP_TEXT, reply_markup=get_help_buttons())

@app.on_callback_query(filters.regex("main_menu"))
async def main_menu_cb(client, query):
    bot = await client.get_me()
    mention = query.from_user.mention
    await query.message.edit_caption(caption=START_TEXT.format(mention=mention, bot_name=bot.first_name), reply_markup=get_start_buttons(bot.username))

@app.on_callback_query(filters.regex(r"h_(.*)"))
async def help_details_cb(client, query):
    cat = query.data.split("_")[1]
    details = {
        "admins": "👑 **Admin Commands:**\n\n/pause - Pause\n/resume - Resume\n/skip - Skip\n/stop - Stop",
        "auth": "🔐 **Auth Commands:**\n\n/auth - Authorize\n/unauth - Unauthorize",
        "blacklist": "🚫 **Blacklist:**\n\n/blacklistchat - Block\n/whitelistchat - Unblock",
        "lang": "🌐 **Language:**\n\n/language - Set language",
        "ping": "🏓 **Ping:**\n\n/ping - Check latency",
        "play": "🎵 **Play:**\n\n/play [song] - Play in VC",
        "queue": "🎼 **Queue:**\n\n/queue - View queue",
        "stats": "📊 **Stats:**\n\n/stats - View stats",
        "sudo": "⚡ **Sudo:**\n\n/gcast - Broadcast\n/addsudo - Add sudo"
    }
    content = details.get(cat, "Select a category!")
    await query.message.edit_caption(caption=content, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help_menu")]]))

# --- PLAY LOGIC ---
from AnonXMusic.plugins.play import play_command
@app.on_message(filters.command(["play", "play@Mdcikbot"]))
async def play_h(client, message):
    await play_command(client, message)

# --- STARTUP ---
async def start_bot():
    logger.info("Starting Refactored AnonXMusic...")
    await init_db()
    await app.start()
    await userbot.start()
    await call_py.start()
    bot = await app.get_me()
    logger.info(f"@{bot.username} is Online! 🚀")
    try:
        await app.send_message(OWNER_ID, f"🚀 **AnonXMusic is Online!**\n\nMode: {'MongoDB' if db else 'Memory'}")
    except: pass
    await idle()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_bot())
