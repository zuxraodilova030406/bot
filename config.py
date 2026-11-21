import os
from typing import List
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load environment variables from .env file inside project root
load_dotenv(os.path.join(BASE_DIR, ".env"))

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "").strip()

# Admin IDs handling: single ID or comma-separated list
_admin_raw = os.getenv("ADMIN_ID", "0").strip()
ADMIN_IDS: List[int] = []
for item in _admin_raw.split(","):
    item = item.strip()
    if item.isdigit():
        ADMIN_IDS.append(int(item))

# Fallback primary admin id
PRIMARY_ADMIN_ID: int = ADMIN_IDS[0] if ADMIN_IDS else 0

def is_admin(user_id: int) -> bool:
    """Check if the given Telegram user_id has administrative privileges."""
    return user_id in ADMIN_IDS

# Brand and Social Configuration
BRAND_NAME: str = os.getenv("BRAND_NAME", "Sarvinoz Collection")
CHANNEL_URL: str = os.getenv("CHANNEL_URL", "https://t.me/Sarvinozcollection1")
CHANNEL_USERNAME: str = os.getenv("CHANNEL_USERNAME", "@Sarvinozcollection1")
ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "@Sarvinoz_admin")

# Database File (Absolute path inside project directory)
_db_filename = os.getenv("DB_NAME", "sarvinoz_collection.db")
DB_NAME: str = os.path.join(BASE_DIR, _db_filename)
