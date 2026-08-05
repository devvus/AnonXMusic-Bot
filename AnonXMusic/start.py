from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import START_IMG_URL, SUPPORT_URL, CHANNEL_URL

@Client.on_message(filters.command("start"))
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
        await message.reply_photo(photo=START_IMG_URL, caption=caption, reply_markup=buttons)
    else:
        await message.reply_text(text=caption, reply_markup=buttons)

@Client.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    await show_help_menu(client, message)

@Client.on_callback_query(filters.regex("help_menu"))
async def help_menu_callback(client: Client, callback_query: CallbackQuery):
    await show_help_menu(client, callback_query.message, edit=True)

@Client.on_callback_query(filters.regex("main_menu"))
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
    
    await callback_query.message.edit_caption(caption=caption, reply_markup=buttons)

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
        await message.edit_caption(caption=caption, reply_markup=buttons)
    else:
        if START_IMG_URL:
            await message.reply_photo(photo=START_IMG_URL, caption=caption, reply_markup=buttons)
        else:
            await message.reply_text(text=caption, reply_markup=buttons)
