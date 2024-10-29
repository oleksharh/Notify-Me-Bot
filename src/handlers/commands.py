from aiogram import types, Router, F
from aiogram.filters import Command
# from aiohttp.web_routedef import options
from bson import ObjectId
from typing import Union
from src.database.db_connect import db
from src.utils.keyboards import MenuCreator
from enum import Enum


# TODO: generalize these status_manage_menu, delete_task_request_menu, priority_manage_menu into one callback_function
# TODO: add error handling, especially in get_reminders, update_task_status, add_reminder


class Priority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2


priority_map = {0: "Low", 1: "Medium", 2: "High"}

menu_creator = MenuCreator()
command_router = Router(name="command_router")


# Welcome command handler function
@command_router.message(Command("start"))
async def send_welcome(message: types.Message) -> None:
    keyboard = menu_creator.user_config_options(message.from_user.id)

    await message.reply(
        "Stay organized with me! But before we begin choose the configuration you want, the default one is:\n"
        "Low Priority: once at 9am\n"
        "Medium Priority: once at 9am and 1pm\n"
        "High Priority: once at 9am and 1pm and 6pm\n"
        "Ultra Priority: every hour from 9am till 11pm\n", reply_markup=keyboard)


@command_router.callback_query(lambda c: c.data.startswith("user_config_"))
async def user_config_handler(callback_query: types.CallbackQuery):
    _, option, user_id = callback_query.data.split(",")

    await callback_query.message.delete()

    if option == "default":
        await db.save_user_info(user_id)
        await callback_query.message.answer("You are all set, stay organized with me!")
        return



# List All Tasks Command Handler
@command_router.message(Command("list"))
async def send_list(message: types.Message) -> None:
    user_id = message.from_user.id
    chat_id = message.chat.id

    reminders = await db.get_reminders(user_id, chat_id)

    if not reminders:
        await message.answer("You are all set, all tasks are finished!")
        return

    tasks_str = format_task_list(reminders)
    keyboard = menu_creator.list_menu()

    await message.answer(text="Your tasks are: \n\n" + tasks_str, reply_markup=keyboard)


def format_task_list(reminders: list) -> str:
    """
    Helper function to format the task list string.
    """

    tasks = [
        f"⚫️ Task ID: {index + 1}\n"
        f"📝 Task: {reminder['message']}\n"
        f"⭐️ Priority: {priority_map.get(reminder['priority'], 'Unknown')}\n"
        for index, reminder in enumerate(reminders)
    ]
    return "\n\n".join(tasks)


# Manage Tasks Callback Query Handler
@command_router.callback_query(lambda c: c.data.startswith("list_"))
async def list_manage(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    function = callback_query.data.split("_")[-1]

    # Remove inline keyboard after selection
    await callback_query.message.edit_reply_markup(reply_markup=None)

    if function == "manage":
        await manage_menu(callback_query.message, user_id, chat_id)
    else:
        await callback_query.message.answer("You are back in the main menu!\n"
                                            "Please enter your next task.")

    await callback_query.answer()


# Manage Menu Command Handler
@command_router.message(Command("manage"))
async def manage_menu(message: types.Message, user_id=0, chat_id=0):
    if user_id == 0 and chat_id == 0:
        user_id = message.from_user.id
        chat_id = message.chat.id

    reminders = await db.get_reminders(user_id, chat_id)

    if not reminders:
        await message.answer("No tasks available.")
        return

    keyboard = menu_creator.manage_menu(reminders)
    await message.answer("Here are your tasks. Choose one to edit:", reply_markup=keyboard)


@command_router.callback_query(lambda c: c.data.startswith("manage_"))
async def edit_task(callback_query: types.CallbackQuery):
    task_id = callback_query.data.split("_")[1]

    await callback_query.message.delete()

    if task_id == "exit":
        await callback_query.message.answer("You are back in the main menu!\n"
                                            "Please enter your next task.")
        return

    task = await db.get_reminder_by_id(task_id)

    if task:
        await callback_query.message.answer(f"You selected: {task['message']}.")
        await edit_menu(callback_query.message, task["_id"])
    else:
        await callback_query.message.answer("Task not found.")

    await callback_query.answer()


async def edit_menu(message: types.Message, task_id: Union[str, ObjectId]):
    keyboard = menu_creator.edit_menu(task_id)
    await message.answer("Choose what you want to perform", reply_markup=keyboard)


async def status_manage_menu(message: types.Message, task_id: Union[str, ObjectId]):
    keyboard = menu_creator.status_manage_menu(task_id)
    await message.answer(text="Choose wanted status", reply_markup=keyboard)


@command_router.callback_query(lambda c: c.data.startswith("status_"))
async def change_status(callback_query: types.CallbackQuery):
    status = bool(callback_query.data.split("_")[1])
    task_id = callback_query.data.split("_")[2]

    await callback_query.message.delete()

    result = await db.update_task_status(task_id, status)
    if result:
        await callback_query.message.answer("Task has been updated.")

    if status:
        await delete_task_request_menu(callback_query.message, task_id)

    await callback_query.answer()


async def delete_task_request_menu(message: types.Message, task_id: Union[str, ObjectId]):
    keyboard = menu_creator.delete_record_menu(task_id)
    await message.answer("Choose if you want to delete the task", reply_markup=keyboard)


@command_router.callback_query(lambda c: c.data.startswith("delete_"))
async def delete_task(callback_query: types.CallbackQuery):
    option = callback_query.data.split("_")[1]
    await callback_query.message.delete()

    if option == "exit":
        await callback_query.message.answer("You are back in the main menu!\n")
        return

    await db.delete_task(option)
    await callback_query.message.answer(f"Task has been deleted.\n"
                                        f"You are back in the main menu!\n")
    await callback_query.answer()


async def priority_manage_menu(message: types.Message, task_id: Union[str, ObjectId]):
    keyboard = menu_creator.priority_manage_menu(task_id)
    await message.answer(text="Choose wanted priority", reply_markup=keyboard)


@command_router.callback_query(lambda c: c.data.startswith("priority_"))
async def change_priority(callback_query: types.CallbackQuery):
    priority = int(callback_query.data.split("_")[1])
    task_id = callback_query.data.split("_")[2]

    await callback_query.message.delete()

    # await callback_query.message.answer(task_id, priority=priority) for DEBUGGING
    result = await db.update_task_priority(task_id, priority)
    if result:
        await callback_query.message.answer(f"Task priority updated to {priority_map[priority]}\n"
                                            "You are back in the main menu!")

    else:
        await callback_query.message.answer("Error has occurred try again later!")
        await callback_query.message.answer("You are back in the main menu!\n")


@command_router.callback_query(lambda c: c.data.startswith("edit_"))
async def edit_task(callback_query: types.CallbackQuery):
    print(callback_query.data)
    function = callback_query.data.split("_")[1]
    task_id = callback_query.data.split("_")[2]

    await callback_query.message.delete()

    if function == "priority":
        await priority_manage_menu(callback_query.message, task_id)
    elif function == "status":
        await status_manage_menu(callback_query.message, task_id)
    else:
        await callback_query.message.answer("Mistake has occurred, check callback_data\n")


# Handle User Text Input
@command_router.message(F.text)
async def handle_user_input(message: types.Message):
    user_input = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id

    # After user input, display the inline menu
    await message.answer("Choose one of the following priorities:",
                         reply_markup=menu_creator.priority_menu(user_id, chat_id, user_input))


# Handle Priority Menu Selection
@command_router.callback_query(lambda c: c.data.startswith("option_"))
async def process_menu_selection(callback_query: types.CallbackQuery):
    selected_option, user_id, chat_id, task_message = callback_query.data.split(",")

    # Remove the message after it's been handled
    await callback_query.message.delete()

    priority = get_priority_from_option(selected_option).value
    print(priority)

    # Upload task to the database
    await db.add_reminder(int(user_id), int(chat_id), task_message, priority)

    await callback_query.answer()
    await callback_query.message.answer("Your task was uploaded to the DB")


def get_priority_from_option(option: str) -> Priority:
    """
    Helper function to map option strings to priority enum values.
    """
    return {
        "option_1": Priority.LOW,
        "option_2": Priority.MEDIUM,
        "option_3": Priority.HIGH
    }.get(option, Priority.HIGH)  # Default to High priority if unrecognized
