import asyncio
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from src.config import BOT_TOKEN
from src.handlers.commands import command_router
from src.database.db_connect import connect_db, close_db, db
from src.utils.scheduled_tasks import ScheduledTasks

# Configure logging
logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    await connect_db()

    tasks = ScheduledTasks(db, bot)
    dp["scheduled_tasks"] = tasks

    dp.include_router(command_router)

    try:
        logging.info("Bot started")
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Critical error: {e}")
    finally:
        logging.info("Shutting down...")
        await dp.storage.close()
        await bot.session.close()
        await close_db()
        logging.info("Shutdown complete")

if __name__ == '__main__':
    asyncio.run(main())