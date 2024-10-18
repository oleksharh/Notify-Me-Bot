from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_priority_menu(user_id, chat_id, message):
    buttons = [
        [InlineKeyboardButton(text="Low", callback_data=f"option_1,{user_id},{chat_id},{message}")],
        [InlineKeyboardButton(text="Medium", callback_data=f"option_2,{user_id},{chat_id},{message}")],
        [InlineKeyboardButton(text="High", callback_data=f"option_3,{user_id},{chat_id},{message}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def create_edit_menu(reminders):
    buttons = [
        [InlineKeyboardButton(text=f"Edit Task {reminder["message"]}", callback_data=f"edit_{reminder["_id"]}")]
        for reminder in reminders
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def create_manage_menu():
    buttons = [
        [InlineKeyboardButton(text=f"Back", callback_data=f"manage_back")],
        [InlineKeyboardButton(text=f"Manage", callback_data=f"manage_manage")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)