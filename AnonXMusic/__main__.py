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

# --- MONGODB FALLBACK LOGIC ---
db = None
state_db = {}

async def init_db():
    global db
    if not MONGO_DB_URI:
        logger.warning("MONGO_DB_URI not found. Falling back to in-memory storage.")
        return
    
    try:
        client = AsyncIOMotorClient(MONGO_DB_URI)
        # Test connection
        await asyncio.wait_for(client.admin.command('ping'), timeout=5.0)
        db = client.AnonXMusic
        logger.info("Successfully connected to MongoDB!")
    except Exception as e:
        logger.error(f"MongoDB connection failed: {e}. Falling back to in-memory storage.")
        db = None

# --- CLIENT INITIALIZATION ---
app = Client(
    "AnonXMusicBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True
)

userbot = TelegramClient(
    StringSession(STRING_SESSION),
    API_ID,
    API_HASH
)

call_py = PyTgCalls(userbot)

# --- UI STRINGS ---
START_TEXT = (
    "Hey {mention},\n"
    "This is {bot_name} !\n\n"
    "A music player bot with some awesome and useful features.\n\n"
    "Click on the help button for more info."
)

HELP_TEXT = (
    "Click the buttons below to get information about my commands.\n\n"
    "Note: All commands can be used with /"
)

# --- HANDLERS ---

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    bot_info = await client.get_me()
    mention = message.from_user.mention
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Add me to your group ➕", url=f"https://t.me/{bot_info.username}?startgroup=true")],
        [InlineKeyboardButton("Help", callback_data="help_menu")],
        [
            InlineKeyboardButton("Support ↗️", url=SUPPORT_CHAT),
            InlineKeyboardButton("Channel ↗️", url=SUPPORT_CHANNEL)
        ]
    ])
    
    try:
        await message.reply_photo(
            photo=START_IMG_URL,
            caption=START_TEXT.format(mention=mention, bot_name=bot_info.first_name),
            reply_markup=buttons
        )
    except Exception:
        await message.reply_text(
            text=START_TEXT.format(mention=mention, bot_name=bot_info.first_name),
            reply_markup=buttons
        )

@app.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    await show_help_menu(client, message)

@app.on_message(filters.command("ping"))
async def ping_command(client: Client, message: Message):
    await message.reply_text("🏓 **Pong! Bot is active and healthy!** ✨")

# --- CALLBACK HANDLERS ---

@app.on_callback_query(filters.regex("help_menu"))
async def help_menu_callback(client: Client, callback_query: CallbackQuery):
    await show_help_menu(client, callback_query.message, edit=True)

@app.on_callback_query(filters.regex("main_menu"))
async def main_menu_callback(client: Client, callback_query: CallbackQuery):
    bot_info = await client.get_me()
    mention = callback_query.from_user.mention
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Add me to your group ➕", url=f"https://t.me/{bot_info.username}?startgroup=true")],
        [InlineKeyboardButton("Help", callback_data="help_menu")],
        [
            InlineKeyboardButton("Support ↗️", url=SUPPORT_CHAT),
            InlineKeyboardButton("Channel ↗️", url=SUPPORT_CHANNEL)
        ]
    ])
    
    try:
        await callback_query.message.edit_caption(
            caption=START_TEXT.format(mention=mention, bot_name=bot_info.first_name),
            reply_markup=buttons
        )
    except Exception:
        await callback_query.message.edit_text(
            text=START_TEXT.format(mention=mention, bot_name=bot_info.first_name),
            reply_markup=buttons
        )

async def show_help_menu(client: Client, message: Message, edit=False):
    # Strict 3-Column Grid Buttons
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Admins", callback_data="h_admins"),
            InlineKeyboardButton("Auth", callback_data="h_auth"),
            InlineKeyboardButton("Blacklist", callback_data="h_blacklist")
        ],
        [
            InlineKeyboardButton("Language", callback_data="h_lang"),
            InlineKeyboardButton("Ping", callback_data="h_ping"),
            InlineKeyboardButton("Play", callback_data="h_play")
        ],
        [
            InlineKeyboardButton("Queue", callback_data="h_queue"),
            InlineKeyboardButton("Stats", callback_data="h_stats"),
            InlineKeyboardButton("Sudoers", callback_data="h_sudo")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ])
    
    if edit:
        try:
            await message.edit_caption(caption=HELP_TEXT, reply_markup=buttons)
        except Exception:
            await message.edit_text(text=HELP_TEXT, reply_markup=buttons)
    else:
        try:
            await message.reply_photo(photo=START_IMG_URL, caption=HELP_TEXT, reply_markup=buttons)
        except Exception:
            await message.reply_text(text=HELP_TEXT, reply_markup=buttons)

@app.on_callback_query(filters.regex(r"h_(.*)"))
async def help_details_callback(client: Client, callback_query: CallbackQuery):
    category = callback_query.data.split("_")[1]
    details = {
        "admins": "👑 **Admin Commands:**\n\n/pause - Pause playback\n/resume - Resume playback\n/skip - Skip track\n/stop - Stop playback",
        "auth": "🔐 **Auth Commands:**\n\n/auth - Authorize user\n/unauth - Unauthorize user\n/authusers - List authorized",
        "blacklist": "🚫 **Blacklist Commands:**\n\n/blacklistchat - Blacklist chat\n/whitelistchat - Whitelist chat",
        "lang": "🌐 **Language Commands:**\n\n/language - Change bot language",
        "ping": "🏓 **Ping Commands:**\n\n/ping - Check latency",
        "play": "🎵 **Play Commands:**\n\n/play [song] - Play music in VC\n/vplay - Video play (if supported)",
        "queue": "🎼 **Queue Commands:**\n\n/queue - View music queue",
        "stats": "📊 **Stats Commands:**\n\n/stats - View bot stats",
        "sudo": "⚡ **Sudo Commands:**\n\n/gcast - Broadcast\n/addsudo - Add sudo\n/delsudo - Remove sudo"
    }
    
    content = details.get(category, "Select a category!")
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help_menu")]])
    
    try:
        await callback_query.message.edit_caption(caption=content, reply_markup=buttons)
    except Exception:
        await callback_query.message.edit_text(text=content, reply_markup=buttons)

# --- PLAY COMMAND HANDLER ---
# Import play logic from plugin (we will refactor play.py next)
try:
    from AnonXMusic.plugins.play import play_command
    @app.on_message(filters.command("play"))
    async def play_h(client, message):
        await play_command(client, message)
except ImportError:
    logger.error("Could not import play_command from plugins.play")

# --- STARTUP ---
async def main():
    logger.info("Initializing AnonXMusic Refactoring...")
    await init_db()
    
    try:
        await app.start()
        bot_info = await app.get_me()
        logger.info(f"Bot started as @{bot_info.username}")
        
        await userbot.start()
        logger.info("Assistant started!")
        
        await call_py.start()
        logger.info("PyTgCalls started!")
        
        try:
            await app.send_message(OWNER_ID, f"🚀 **AnonXMusic Refactored is Online!**\n\nDatabase: {'MongoDB' if db else 'In-Memory'}")
        except:
            pass
            
        await idle()
    except Exception as e:
        logger.error(f"Startup Error: {e}")
    finally:
        if app.is_connected: await app.stop()
        if userbot.is_connected(): await userbot.disconnect()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
