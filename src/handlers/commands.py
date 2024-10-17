from aiogram import types, Router
from aiogram.filters import Command
from src.database.db_connection import db
command_router = Router(name=__name__)
@command_router.message(Command('start'))
async def send_welcome(message: types.Message):
    reminder_collection = db["reminders"]
    reminders = await reminder_collection.find().to_list(length=None)

    print(reminders)

    await message.reply(f"Hello! Welcome to the bot. Here are your reminders: {reminders}")
