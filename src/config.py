# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env.local
load_dotenv('.env.local')

# Bot configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
MONGODB_URI = os.getenv('MONGODB_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')

MAX_REMINDERS_PER_USER = 10
EXEMPT_USER_IDS = int(os.getenv('EXEMPT_USER_IDS'))
