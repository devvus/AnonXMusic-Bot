import asyncio
import logging
import os
from pyrogram import Client, idle, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telethon import TelegramClient
from telethon.sessions import StringSession
from pytgcalls import PyTgCalls
from config import API_ID, API_HASH, STRING_SESSION, BOT_TOKEN, OWNER_ID, START_IMG_URL, SUPPORT_URL, CHANNEL_URL

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(name)s: %(message)s")
logger = logging.getLogger("AnonXMusic")

# Initialize Pyrogram Bot Client
# We initialize without plugins root to handle everything here for maximum reliability
app = Client(
    "AnonXBotFinal",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True
)

# Initialize Telethon Assistant Client
userbot = TelegramClient(
    StringSession(STRING_SESSION),
    API_ID,
    API_HASH
)

# Initialize PyTgCalls with Telethon client
call_py = PyTgCalls(userbot)

# --- UI STRINGS & HELPERS ---

START_TEXT = (
    "✨ **Hey {mention}**, \n\n"
    "🌸 **This is {bot_name}** ! 🎶\n\n"
    "🎀 **A fast and powerful music player bot for Telegram voice chats.**\n\n"
    "💖 **Enjoy high-quality music with your friends! Click the buttons below for more info.** ✨"
)

HELP_TEXT = (
    "✨ **Click the buttons below to explore my commands!** 🌸\n\n"
    "📌 **Note:** All commands can be used with a `/` prefix."
)

# --- HANDLERS ---

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    bot_info = await client.get_me()
    bot_name = bot_info.first_name
    bot_username = bot_info.username
    mention = message.from_user.mention
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add me to your group ➕", url=f"https://t.me/{bot_username}?startgroup=true")],
        [InlineKeyboardButton("📜 Help & Commands 📜", callback_data="help_menu")],
        [InlineKeyboardButton("💬 Support ↗️", url=SUPPORT_URL), InlineKeyboardButton("📢 Channel ↗️", url=CHANNEL_URL)]
    ])
    
    if START_IMG_URL:
        try:
            await message.reply_photo(
                photo=START_IMG_URL,
                caption=START_TEXT.format(mention=mention, bot_name=bot_name),
                reply_markup=buttons
            )
        except Exception as e:
            logger.error(f"Error sending start photo: {e}")
            await message.reply_text(
                text=START_TEXT.format(mention=mention, bot_name=bot_name),
                reply_markup=buttons
            )
    else:
        await message.reply_text(
            text=START_TEXT.format(mention=mention, bot_name=bot_name),
            reply_markup=buttons
        )

@app.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    await show_help_menu(client, message)

@app.on_message(filters.command("ping"))
async def ping_command(client, message):
    await message.reply_text("🏓 **Pong! Bot is active and healthy!** ✨")

# --- CALLBACK HANDLERS ---

@app.on_callback_query(filters.regex("help_menu"))
async def help_menu_callback(client: Client, callback_query: CallbackQuery):
    await show_help_menu(client, callback_query.message, edit=True)

@app.on_callback_query(filters.regex("main_menu"))
async def main_menu_callback(client: Client, callback_query: CallbackQuery):
    bot_info = await client.get_me()
    bot_name = bot_info.first_name
    bot_username = bot_info.username
    mention = callback_query.from_user.mention
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add me to your group ➕", url=f"https://t.me/{bot_username}?startgroup=true")],
        [InlineKeyboardButton("📜 Help & Commands 📜", callback_data="help_menu")],
        [InlineKeyboardButton("💬 Support ↗️", url=SUPPORT_URL), InlineKeyboardButton("📢 Channel ↗️", url=CHANNEL_URL)]
    ])
    
    try:
        await callback_query.message.edit_caption(
            caption=START_TEXT.format(mention=mention, bot_name=bot_name),
            reply_markup=buttons
        )
    except Exception:
        await callback_query.message.edit_text(
            text=START_TEXT.format(mention=mention, bot_name=bot_name),
            reply_markup=buttons
        )

@app.on_callback_query(filters.regex(r"help_(.*)"))
async def help_category_callback(client: Client, callback_query: CallbackQuery):
    category = callback_query.data.split("_")[1]
    
    # Simple help content for each category
    help_contents = {
        "admins": "👑 **Admin Commands:**\n\n/pause - Pause playback\n/resume - Resume playback\n/skip - Skip current track\n/stop - Stop playback",
        "auth": "🔐 **Auth Commands:**\n\n/auth - Authorize a user\n/unauth - Unauthorize a user\n/authusers - List authorized users",
        "blacklist": "🚫 **Blacklist Commands:**\n\n/blacklistchat - Blacklist a chat\n/whitelistchat - Whitelist a chat\n/blacklistedchats - List blacklisted chats",
        "lang": "🌐 **Language Commands:**\n\n/language - Change bot language",
        "ping": "🏓 **Ping Commands:**\n\n/ping - Check bot latency and status",
        "play": "🎵 **Play Commands:**\n\n/play [song name/link] - Play music in voice chat",
        "queue": "🎼 **Queue Commands:**\n\n/queue - View current music queue",
        "stats": "📊 **Stats Commands:**\n\n/stats - View bot statistics",
        "sudo": "⚡ **Sudo Commands:**\n\n/gcast - Broadcast a message\n/addsudo - Add a sudo user\n/delsudo - Remove a sudo user"
    }
    
    content = help_contents.get(category, "🌸 Select a category for more info!")
    
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="help_menu")]])
    
    try:
        await callback_query.message.edit_caption(caption=content, reply_markup=buttons)
    except Exception:
        await callback_query.message.edit_text(text=content, reply_markup=buttons)

async def show_help_menu(client: Client, message: Message, edit=False):
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👑 Admins", callback_data="help_admins"),
            InlineKeyboardButton("🔐 Auth", callback_data="help_auth"),
            InlineKeyboardButton("🚫 Blacklist", callback_data="help_blacklist")
        ],
        [
            InlineKeyboardButton("🌐 Language", callback_data="help_lang"),
            InlineKeyboardButton("🏓 Ping", callback_data="help_ping"),
            InlineKeyboardButton("🎵 Play", callback_data="help_play")
        ],
        [
            InlineKeyboardButton("🎼 Queue", callback_data="help_queue"),
            InlineKeyboardButton("📊 Stats", callback_data="help_stats"),
            InlineKeyboardButton("⚡ Sudoers", callback_data="help_sudo")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ])
    
    if edit:
        try:
            await message.edit_caption(caption=HELP_TEXT, reply_markup=buttons)
        except Exception:
            await message.edit_text(text=HELP_TEXT, reply_markup=buttons)
    else:
        if START_IMG_URL:
            try:
                await message.reply_photo(photo=START_IMG_URL, caption=HELP_TEXT, reply_markup=buttons)
            except Exception:
                await message.reply_text(text=HELP_TEXT, reply_markup=buttons)
        else:
            await message.reply_text(text=HELP_TEXT, reply_markup=buttons)

# --- PLAY LOGIC (Integrated for reliability) ---

from AnonXMusic.plugins.play import play_command
@app.on_message(filters.command("play"))
async def play_handler(client, message):
    await play_command(client, message)

# --- MAIN STARTUP ---

async def main():
    logger.info("Starting AnonXMusic Bot...")
    try:
        # Start Pyrogram Bot
        await app.start()
        bot_info = await app.get_me()
        logger.info(f"Pyrogram Bot Client started as @{bot_info.username}")
        
        # Start Telethon Assistant
        await userbot.start()
        logger.info("Telethon Assistant Client started!")
        
        # Start PyTgCalls
        await call_py.start()
        logger.info("PyTgCalls Client started!")

        # Send startup message to Owner
        try:
            await app.send_message(OWNER_ID, f"🚀 **Bot @{bot_info.username} is online with Cute Anime UI!** ✨")
        except Exception as e:
            logger.error(f"Could not send startup message: {e}")

        logger.info("Bot is fully online and listening for messages...")
        
        await idle()
        
    except Exception as e:
        logger.error(f"Critical error during startup: {e}", exc_info=True)
    finally:
        # Graceful shutdown
        if app.is_connected:
            await app.stop()
        if userbot.is_connected():
            await userbot.disconnect()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
