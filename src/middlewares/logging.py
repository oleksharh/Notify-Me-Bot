from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

class CustomMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        # Example custom middleware logic here
        print(f"Handling event: {event}")
        return await handler(event, data)

# To register middleware in your bot.py:
# dp.message.middleware(CustomMiddleware())
