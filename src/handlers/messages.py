from aiogram import types
from src.bot import dp

@dp.message_handler()
async def echo_message(message: types.Message):
    await message.answer(message.text)
