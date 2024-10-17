import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

# Load environment variables from .env.local
load_dotenv('.env.local')

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Fetch the API token from environment variables
API_TOKEN = os.getenv("API_TOKEN")

if not API_TOKEN:
    raise ValueError("No API token found. Please add your bot token to .env.local.")

# Initialize bot
bot = Bot(token=API_TOKEN)
# Initialize dispatcher and associate it with the bot instance
dp = Dispatcher()

from handlers.commands import command_router
dp.include_router(command_router)
