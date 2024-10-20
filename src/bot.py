import logging
from aiogram import Bot, Dispatcher
from config import API_TOKEN

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize bot
bot = Bot(token=API_TOKEN)

# Initialize dispatcher (no need to pass bot here)
dp = Dispatcher()

# Include routers (modular command handlers)
from handlers.commands import command_router
dp.include_router(command_router)

# Expose bot and dispatcher for use in other modules when importing
__all__ = ["bot", "dp"]
