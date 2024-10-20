import asyncio
import logging
from bot import bot, dp

async def main() -> None:
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Error occurred during polling: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
