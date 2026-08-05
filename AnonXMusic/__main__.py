import asyncio
import logging
import os
from pyrogram import Client, idle, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telethon import TelegramClient
from telethon.sessions import StringSession
from pytgcalls import PyTgCalls
from config import API_ID, API_HASH, STRING_SESSION, BOT_TOKEN, OWNER_ID, START_IMG_URL, SUPPORT_URL, CHANNEL_URL
from AnonXMusic.plugins.play import play_command

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(name)s: %(message)s")
logger = logging.getLogger("AnonXMusic")

# Initialize Pyrogram Bot Client (No plugins root to avoid conflicts)
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

# --- HANDLERS ---

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    bot_info = await client.get_me()
    bot_name = bot_info.first_name
    bot_username = bot_info.username
    user_mention = message.from_user.mention
    
    caption = (
        f"✨ Hey {user_mention},\n"
        f"🌸 This is {bot_name} ! 🎶\n\n"
        f"🎀 A music player bot with some awesome and useful features!\n\n"
        f"💖 Click on the help button for more info ✨"
    )
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add me to your group ➕", url=f"https://t.me/{bot_username}?startgroup=true")],
        [InlineKeyboardButton("📜 Help & Commands 📜", callback_data="help_menu")],
        [InlineKeyboardButton("💬 Support ↗️", url=SUPPORT_URL), InlineKeyboardButton("📢 Channel ↗️", url=CHANNEL_URL)]
    ])
    
    if START_IMG_URL:
        try:
            await message.reply_photo(photo=START_IMG_URL, caption=caption, reply_markup=buttons)
        except Exception:
            await message.reply_text(text=caption, reply_markup=buttons)
    else:
        await message.reply_text(text=caption, reply_markup=buttons)

@app.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    await show_help_menu(client, message)

@app.on_callback_query(filters.regex("help_menu"))
async def help_menu_callback(client: Client, callback_query: CallbackQuery):
    await show_help_menu(client, callback_query.message, edit=True)

@app.on_callback_query(filters.regex("main_menu"))
async def main_menu_callback(client: Client, callback_query: CallbackQuery):
    bot_info = await client.get_me()
    bot_name = bot_info.first_name
    bot_username = bot_info.username
    user_mention = callback_query.from_user.mention
    
    caption = (
        f"✨ Hey {user_mention},\n"
        f"🌸 This is {bot_name} ! 🎶\n\n"
        f"🎀 A music player bot with some awesome and useful features!\n\n"
        f"💖 Click on the help button for more info ✨"
    )
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add me to your group ➕", url=f"https://t.me/{bot_username}?startgroup=true")],
        [InlineKeyboardButton("📜 Help & Commands 📜", callback_data="help_menu")],
        [InlineKeyboardButton("💬 Support ↗️", url=SUPPORT_URL), InlineKeyboardButton("📢 Channel ↗️", url=CHANNEL_URL)]
    ])
    
    try:
        await callback_query.message.edit_caption(caption=caption, reply_markup=buttons)
    except Exception:
        await callback_query.message.edit_text(text=caption, reply_markup=buttons)

async def show_help_menu(client: Client, message: Message, edit=False):
    caption = (
        "✨ Click the buttons below to get information about my commands! 🌸\n\n"
        "📌 Note: All commands can be used with /"
    )
    
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
            await message.edit_caption(caption=caption, reply_markup=buttons)
        except Exception:
            await message.edit_text(text=caption, reply_markup=buttons)
    else:
        if START_IMG_URL:
            try:
                await message.reply_photo(photo=START_IMG_URL, caption=caption, reply_markup=buttons)
            except Exception:
                await message.reply_text(text=caption, reply_markup=buttons)
        else:
            await message.reply_text(text=caption, reply_markup=buttons)

@app.on_message(filters.command("ping"))
async def ping_command(client, message):
    await message.reply_text("🏓 Pong! Bot is active and healthy! ✨")

# Manually register the play command from the plugin
@app.on_message(filters.command("play"))
async def play_handler(client, message):
    await play_command(client, message)

# --- MAIN STARTUP ---

async def main():
    logger.info("Starting bot and assistant (Telethon)...")
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
            await app.send_message(OWNER_ID, f"🚀 Bot @{bot_info.username} is online with Telethon Assistant on Railway!")
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
