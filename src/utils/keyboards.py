from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bson import ObjectId


def create_priority_menu(user_id, chat_id, message):
    buttons = [
        [InlineKeyboardButton(text="Low", callback_data=f"option_1,{user_id},{chat_id},{message}")],
        [InlineKeyboardButton(text="Medium", callback_data=f"option_2,{user_id},{chat_id},{message}")],
        [InlineKeyboardButton(text="High", callback_data=f"option_3,{user_id},{chat_id},{message}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_manage_menu(reminders):
    buttons = [
        [InlineKeyboardButton(text="🚪 Exit", callback_data="manage_exit")],
        *[
            [InlineKeyboardButton(text=f"Edit Task {reminder['message']}", callback_data=f"manage_{reminder['_id']}")]
            for reminder in reminders
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_list_menu():
    buttons = [
        [InlineKeyboardButton(text=f"Back", callback_data=f"list_back")],
        [InlineKeyboardButton(text=f"Manage", callback_data=f"list_manage")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_edit_menu(task_id: str | ObjectId):
    buttons = [
        [InlineKeyboardButton(text=f"Manage Priority", callback_data=f"edit_priority_{task_id}")],
        [InlineKeyboardButton(text=f"Set task as finished", callback_data=f"edit_status_{task_id}")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_priority_manage_menu(task_id: str | ObjectId):
    buttons = [
        [InlineKeyboardButton(text=f"Low", callback_data=f"priority_1_{task_id}")],
        [InlineKeyboardButton(text=f"Medium", callback_data=f"priority_2_{task_id}")],
        [InlineKeyboardButton(text=f"High", callback_data=f"priority_3_{task_id}")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)

def create_status_manage_menu(task_id: str | ObjectId):
    buttons = [
        [InlineKeyboardButton(text=f"Not Finished", callback_data=f"status_false_{task_id}")],
        [InlineKeyboardButton(text=f"Finished", callback_data=f"status_true_{task_id}")],
    ]
