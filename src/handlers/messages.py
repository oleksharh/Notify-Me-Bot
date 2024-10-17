from aiogram import types, Router

message_router = Router(name=__name__)
@message_router.message()
async def echo_message(message: types.Message):
    await message.answer(message.text)
