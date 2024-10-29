from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bson import ObjectId
from typing import Union


class MenuCreator:
    def __init__(self):
        pass

    @staticmethod
    def create_buttons(options: list[tuple], callback_format: str) -> InlineKeyboardMarkup:
        """
        Generic function to create buttons from a list of options.

        :param options: A list of tuples where each tuple contains (text, callback_identifier).
        :param callback_format: The callback data format where the identifier will be inserted.
        :return: InlineKeyboardMarkup with generated buttons.
        """
        buttons = [
            [InlineKeyboardButton(text=text, callback_data=callback_format.format(callback_identifier))]
            for text, callback_identifier in options
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def priority_menu(user_id, chat_id, message):
        options = [
            ("Low", 1),
            ("Medium", 2),
            ("High", 3)
        ]
        callback_format = f"option_{{}},{user_id},{chat_id},{message}"
        return MenuCreator.create_buttons(options, callback_format)

    @staticmethod
    def manage_menu(reminders):
        options = [("🚪 Exit", "exit")] + [(f"Edit Task {reminder['message']}", reminder['_id']) for reminder in
                                          reminders]
        callback_format = "manage_{}"
        return MenuCreator.create_buttons(options, callback_format)

    @staticmethod
    def list_menu():
        options = [("Back", "back"), ("Manage", "manage")]
        callback_format = "list_{}"
        return MenuCreator.create_buttons(options, callback_format)

    @staticmethod
    def edit_menu(task_id: Union[str, ObjectId]):
        options = [
            ("Manage Priority", f"priority_{task_id}"),
            ("Set task status", f"status_{task_id}")
        ]
        callback_format = "edit_{}"
        return MenuCreator.create_buttons(options, callback_format)

    @staticmethod
    def priority_manage_menu(task_id: Union[str, ObjectId]):
        options = [
            ("Low", 0),
            ("Medium", 1),
            ("High", 2)
        ]
        callback_format = f"priority_{{}}_{task_id}"
        return MenuCreator.create_buttons(options, callback_format)

    @staticmethod
    def status_manage_menu(task_id: Union[str, ObjectId]):
        options = [
            ("Not Finished", "false"),
            ("Finished", "true")
        ]
        callback_format = f"status_{{}}_{task_id}"
        return MenuCreator.create_buttons(options, callback_format)

    @staticmethod
    def delete_record_menu(task_id: Union[str, ObjectId]):
        options = [
            ("🚪 Exit to the menu", "exit"),
            ("Delete Task", f"{task_id}"),
        ]
        callback_format = "delete_{}"
        return MenuCreator.create_buttons(options, callback_format)


    @staticmethod
    def user_config_options(user_id: int):
        options = [
            ("Default", "default"),
            ("Configure", "configure"),
        ]
        callback_format = f"user_config_,{{}},{user_id}"
        return MenuCreator.create_buttons(options, callback_format)

    @staticmethod
    def user_config():
        options = [
            ("Low", "low"),
            ("Medium", "medium"),
            ("High", "high"),
            ("Ultra", "ultra"),
        ]
        callback_format = "config_{}"
        return MenuCreator.create_buttons(options, callback_format)