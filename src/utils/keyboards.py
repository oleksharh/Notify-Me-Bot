from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bson import ObjectId
from typing import Union, Tuple


class MenuCreator:
    def __init__(self):
        pass

    @staticmethod
    def create_buttons(options: list[Tuple[str, Union[str, int]]], callback_format: str, row_width: int = None) -> InlineKeyboardMarkup:
        """
        Generic function to create buttons from a list of options.

        :param row_width: A width of a row (simply put that's how many buttons will be in line)
        :param options: A list of tuples where each tuple contains (text, callback_identifier).
        :param callback_format: The callback data format where the identifier will be inserted.
        :return: InlineKeyboardMarkup with generated buttons.
        """
        buttons = []
        current_row = []

        for text, callback_identifier in options:
            # Create button with callback data
            button = InlineKeyboardButton(text=text, callback_data=callback_format.format(callback_identifier))
            current_row.append(button)

            # Add row when it reaches the row_width limit
            if row_width and len(current_row) == row_width:
                buttons.append(current_row)
                current_row = []

        # Add remaining buttons in columns if no row_width, or as the last row
        if current_row:
            if row_width:
                buttons.append(current_row)
            else:
                buttons.extend([[button] for button in current_row])

        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def user_config_options(user_id: int):
        options = [
            ("Default", "default"),
            ("Configure", "configure"),
        ]
        callback_format = f"user_config_,{{}},{user_id}"
        return MenuCreator.create_buttons(options, callback_format, 2)

    @staticmethod
    def priority_menu(object_id: Union[str, ObjectId]) -> InlineKeyboardMarkup:
        options = [
            ("Low", "low"),
            ("Medium", "medium"),
            ("High", "high"),
            ("Ultra", "ultra"),
        ]
        callback_format = f"option_{{}},{object_id}"
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
    def user_config():
        options = [
            ("Back to the main menu", "exit"),
            ("Low", "low"),
            ("Medium", "medium"),
            ("High", "high"),
            ("Ultra", "ultra"),
        ]
        callback_format = "config_{}"
        return MenuCreator.create_buttons(options, callback_format)

    @staticmethod
    def dayparts():
        options = [
            ("Back to the main menu", "exit"),
            ("Morning", 0),
            ("Afternoon", 1),
            ("Evening", 2),
            ("Ultra", 3),
        ]

        callback_format = "daypart_{}"
        return MenuCreator.create_buttons(options, callback_format, 2)

    @staticmethod
    def times_config(hr_from: int, hr_to: int, daypart: int):
        """
        :param daypart: part of the day that was chosen in the dayparts function.
        :param hr_from: hour that count will start from.
        :param hr_to: hour that count will end at (Excluding the hr_to, so will show on the buttons hr_to - 1).
        :return: InlineKeyboardMarkup with buttons inside it.
        """
        options = []

        # Generate options for each hour, with three options per row
        for hour in range(hr_from, hr_to, 1):
            options.append((f"{hour}:00", f"{hour}_{daypart}"))

        # Create buttons using the existing create_buttons method
        return MenuCreator.create_buttons(options, "times_config_{}", 4)

