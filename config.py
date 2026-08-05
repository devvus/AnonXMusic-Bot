import os

API_ID = int(os.getenv("API_ID", "21846639"))
API_HASH = os.getenv("API_HASH", "2cebc99bd8378b5237b31ea8e7496d79")
STRING_SESSION = os.getenv("STRING_SESSION", "BQFNWm8AorDYUR9k5bQi6prBuBazl2Wr-_KzM2L6uv_1pMR5BJvWdgdQneNFTalulSOoKrwgpCSpfo86JjzEG8-gg0Zd1fSIyNLkfERGuMgS_3dWJNhdI_gkhjEMAQ4H-iBmqY-FqvhQ2Xv774LN-FOjD7KnMnT65SeTFCKJg4dX3oavyBpHliS9btVFT2w3c7Dff-lWD48yrB2S1SQbIYEWQ0dYHv87DS18ekg1LBZ7uCPowE9PgDoxNjXpoSFLmltvxF2l5gZEONYgIixNalm2_OxyRdx3qHMgyP_sLmwgqBiXvFI4KiO-B-o5bCAVK-4I8HVBl-IHOt5M5wPJKZhInWzTdgAAAABsFeBfAA")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8913524572:AAEVVBg7Aq2G5A8uaI-wjYMIVGWjujTLn-A")
OWNER_ID = int(os.getenv("OWNER_ID", "1499705163"))
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", "-1001973634248"))
LOG_CHAT_ID = int(os.getenv("LOG_CHAT_ID", "-1004356536394"))
MONGO_DB_URI = os.getenv("MONGO_DB_URI", "mongodb+srv://Devvusz:Devvuszxx05231@cluster0.3rfouod.mongodb.net/?appName=Cluster0")

# Fallback for in-memory state if MongoDB is not used
if not MONGO_DB_URI:
    print("MongoDB URI not provided. Bot will use in-memory storage.")
    # You might want to define a simple in-memory storage here if needed
    # For now, we'll just print a message and let the bot handle it.
