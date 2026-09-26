import os

# 1️⃣ Yahan apna Bot Token daalo (BotFather se milega)
BOT_TOKEN = os.getenv("BOT_TOKEN", "8292476628:AAGx-5whEPP7oR_lTWzVn-ciq1KYWRbhnvU")

# 2️⃣ Yahan apni Telegram User ID daalo (comma se multiple)
ADMIN_ID = "6830366019"  # ← isko apni ID se replace karo

# 3️⃣ Ye 2 lines API ke liye — CLIENT_KEY change karo
API_BASE = "https://techvishalboss.com/api/v1/lookup.php"
CLIENT_KEY = "TVB_FULL_E38A6225"   # ← ye change karo
DEFAULT_SERVICE = "number"

DB_PATH = "data/bot.db"
