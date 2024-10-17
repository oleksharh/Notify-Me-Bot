from aiogram import types, Router
from aiogram.filters import Command

command_router = Router(name=__name__)
@command_router.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.reply("Hello! Welcome to the bot.")

@command_router.message(Command('help'))
async def send_help(message: types.Message):
    await message.reply("Available commands:\n/start - Welcome message\n/help - Show available commands")
