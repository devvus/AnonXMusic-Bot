import os
from dotenv import load_dotenv

load_dotenv()

# API Credentials
API_ID = int(os.getenv("API_ID", "21846639"))
API_HASH = os.getenv("API_HASH", "2cebc99bd8378b5237b31ea8e7496d79")

# Bot & Assistant Tokens
BOT_TOKEN = os.getenv("BOT_TOKEN", "8913524572:AAEVVBg7Aq2G5A8uaI-wjYMIVGWjujTLn-A")
STRING_SESSION = os.getenv("STRING_SESSION", "1BVtsOKEBu4xzILcEjJ9Qx9cQS7SeOD1OMhx1iGdhPhOW7dXP1KLGPyZa6ynFLJO-af8yUJLMQFvSKyNQWmQvqwhe4TdNuncC9oQ-Ev_5aw-i8uFpe0_rFKOgCQ4pf7NIfkrKHEoa3LcW6pfQ_I9Lb-gzLbcTyAL7UI4gsqUf-INLzpysbKFjrAiaKPB_WkKtpTcskIR4cEc0ihy25rl9sHk19WUv5uq5HlQmo9vnAqGBeRF-k0xUBZGwTDWOYsnQcwAExo2CFqKGmhEgH6mnl8yJEKoT2CCEEQj4eEobR6LeN8CLSqMMtqNKMYCAuLv4TFc1oJGH4qw82gfJRvp-oH926CPBNQ4=")

# IDs
OWNER_ID = int(os.getenv("OWNER_ID", "1499705163"))
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", "-1001973634248"))
LOG_CHAT_ID = int(os.getenv("LOG_CHAT_ID", "-1004356536394"))

# Database
MONGO_DB_URI = os.getenv("MONGO_DB_URI", "mongodb+srv://Devvusz:Devvuszxx05231@cluster0.3rfouod.mongodb.net/?appName=Cluster0")

# Branding & Links
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "https://t.me/XD_NETW0RK")
SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "https://t.me/XD_NETW0RK")
START_IMG_URL = os.getenv("START_IMG_URL", "https://images.alphacoders.com/131/1312385.jpeg")

# Compatibility Aliases (for old code)
SUPPORT_URL = SUPPORT_CHAT
CHANNEL_URL = SUPPORT_CHANNEL

# yt-dlp Configuration
COOKIES_FILE_PATH = os.path.join(os.getcwd(), "cookies.txt")
