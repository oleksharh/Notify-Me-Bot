from aiogram import types, Router, F
from aiogram.filters import Command
from bson import ObjectId

from src.database.db_operations import add_reminder, get_reminders, get_reminder_by_id, remove_reminder, \
    update_task_status
from src.utils.keyboards import create_manage_menu, create_priority_menu, create_list_menu, create_edit_menu, \
    create_priority_manage_menu, create_status_manage_menu

command_router = Router(name="command_router")


########################################
###          COMMAND HANDLERS        ###
########################################

# Welcome command handler function
@command_router.message(Command("start"))
async def send_welcome(message: types.Message) -> None:
    await message.reply("Stay organized with me! Just drop a message "
                        "in the chat and I will sort it out for you!")


# List All Tasks Command Handler
@command_router.message(Command("list"))
async def send_list(message: types.Message) -> None:
    user_id = message.from_user.id
    chat_id = message.chat.id

    reminders = await get_reminders(user_id, chat_id)

    if not reminders:
        await message.answer("You are all set, all tasks are finished!")
        return

    tasks_str = format_task_list(reminders)
    keyboard = create_list_menu()

    await message.answer(text="Your tasks are: \n\n" + tasks_str, reply_markup=keyboard)


def format_task_list(reminders: list) -> str:
    """
    Helper function to format the task list string.
    """
    priority_map = {0: "Low", 1: "Medium", 2: "High"}

    tasks = [
        f"⚫️ Task ID: {index + 1}\n"
        f"📝 Task: {reminder['message']}\n"
        f"⭐️ Priority: {priority_map.get(reminder['priority'], "Unknown")}\n"
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

    reminders = await get_reminders(user_id, chat_id)

    if not reminders:
        await message.answer("No tasks available.")
        return

    keyboard = create_manage_menu(reminders)
    await message.answer("Here are your tasks. Choose one to edit:", reply_markup=keyboard)


@command_router.callback_query(lambda c: c.data.startswith("manage_"))
async def edit_task(callback_query: types.CallbackQuery):
    task_id = callback_query.data.split("_")[1]

    await  callback_query.message.delete()

    if task_id == "exit":
        await callback_query.message.answer("You are back in the main menu!\n"
                                            "Please enter your next task.")
        return

    task = await get_reminder_by_id(task_id)

    if task:
        await callback_query.message.answer(f"You selected: {task["message"]}. {type(task["_id"])}")
        await edit_menu(callback_query.message, task["_id"])
    else:
        await callback_query.message.answer("Task not found.")

    await callback_query.answer()


async def edit_menu(message: types.Message, task_id: str | ObjectId):
    keyboard = create_edit_menu(task_id)
    await message.answer("Choose what you want to perform", reply_markup=keyboard)


def change_status(message: types.Message, task_id: str | ObjectId, status: bool):

    update_task_status(task_id, status)


def change_priority(message: types.Message, task_id: str | ObjectId, priority: int):
    pass


@command_router.callback_query(lambda c: c.data.startswith("edit_"))
async def edit_task(callback_query: types.CallbackQuery):
    function = callback_query.data.split("_")[1]
    task_id = callback_query.data.split("_")[2]

    await callback_query.message.delete()

    if function == "priority":
        keyboard = create_priority_manage_menu(task_id)
        await callback_query.message.edit_reply_markup(text="Choose wanted priority",reply_markup=None)
        change_priority(callback_query.message, task_id, 0)
    elif function == "status":
        keyboard = create_status_manage_menu(task_id)
        await callback_query.message.edit_reply_markup(reply_markup=None)
        # change_status(task_id,)
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
                         reply_markup=create_priority_menu(user_id, chat_id, user_input))


# Handle Priority Menu Selection
@command_router.callback_query(lambda c: c.data.startswith("option_"))
async def process_menu_selection(callback_query: types.CallbackQuery):
    selected_option, user_id, chat_id, task_message = callback_query.data.split(",")

    # Remove the message after it's been handled
    await callback_query.message.delete()

    priority = get_priority_from_option(selected_option)

    # Upload task to the database
    await add_reminder(int(user_id), int(chat_id), task_message, int(priority))

    await callback_query.answer()
    await callback_query.message.answer("Your task was uploaded to the DB")


def get_priority_from_option(option: str) -> int:
    """
    Helper function to map option strings to priority values.
    """
    return {
        "option_1": 0,  # Low priority
        "option_2": 1,  # Medium priority
        "option_3": 2  # High priority
    }.get(option, 2)  # Default to High priority if unrecognized
