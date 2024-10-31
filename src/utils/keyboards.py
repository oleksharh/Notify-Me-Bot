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
        # buttons = []  # Initialize the button list
        #
        # # Create a row to hold buttons
        # current_row = []
        #
        # for i, (text, callback_identifier) in enumerate(options):
        #     # Create a button
        #     button = InlineKeyboardButton(text=text, callback_data=callback_format.format(callback_identifier))
        #
        #     # Append button to the current row
        #     current_row.append(button)
        #
        #     # If row_width is set and current row is full, add it to buttons and start a new row
        #     if row_width is not None and (i + 1) % row_width == 0:
        #         buttons.append(current_row)  # Add the current row to buttons
        #         current_row = []  # Start a new row
        #
        # # Add the last row if it has any buttons
        # if current_row:
        #     buttons.append(current_row)
        #
        # return InlineKeyboardMarkup(inline_keyboard=buttons)
        # TODO: FIX ABOVE METHOD


    @staticmethod
    def priority_menu(object_id: Union[str, ObjectId]) -> InlineKeyboardMarkup:
        options = [
            ("Low", 1),
            ("Medium", 2),
            ("High", 3)
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

    @staticmethod
    def times_config():
        options = []

        # Generate options for each hour, with three options per row
        for i in range(0, 24, 3):
            row = []
            for j in range(3):
                hour = i + j
                if hour < 24:  # Ensure the hour is valid
                    row.append((f"{hour}:00", f"{hour}"))
            options.append(row)

        flat_options = [item for sublist in options for item in sublist]

        # Create buttons using the existing create_buttons method
        return MenuCreator.create_buttons(flat_options, "times_config_{}")

