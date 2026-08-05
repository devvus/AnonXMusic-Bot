import os

API_ID = int(os.getenv("API_ID", "2cebc99bd8378b5237b31ea8e7496d79"))
API_HASH = os.getenv("API_HASH", "2cebc99bd8378b5237b31ea8e7496d79")
STRING_SESSION = os.getenv("STRING_SESSION", "BQFNWm8AXgFl0DopZqvwxcFQBvu9Fp_TAOFpWYz3scJfkocXcef0WLe1Yg4M51yhW_eKjHsGJG3caHwXaxkea9ERh2Y7aFcXdA3qWPerdRFk7ULs76EN4nsXT6dFGcYeb7UuCUDz3mSDdijc9_6XYJi1-QoBuMrLWDH6zzBUBzq0WZCj5EY1v4DWvYY5q1e3RQx6ZRsC0S5l3mN2EMXIIQ2rlG7qPqcjNL6PqyRX6_wBb4UjghI5GjvWqbrFXfOPRnB_YxvJ1aOzNrNed7uY96spBVPlNJuSe-QqS69yEz7buTs0VY9SMbyZIU4ph2cWXPmdwKYGoPtY4yB0zjOI6BWuXA1b2AAAAABsFeBfAA")
OWNER_ID = int(os.getenv("OWNER_ID", "1499705163"))
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", "-1001973634248"))
LOG_CHAT_ID = int(os.getenv("LOG_CHAT_ID", "-1004356536394"))
MONGO_DB_URI = os.getenv("MONGO_DB_URI", "mongodb+srv://Devvusz:Devvuszxx05231@cluster0.3rfouod.mongodb.net/?appName=Cluster0")

# Fallback for in-memory state if MongoDB is not used
if not MONGO_DB_URI:
    print("MongoDB URI not provided. Bot will use in-memory storage.")
    # You might want to define a simple in-memory storage here if needed
    # For now, we'll just print a message and let the bot handle it.
