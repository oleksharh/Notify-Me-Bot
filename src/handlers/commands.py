from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bson import ObjectId
import json

from src.database.db_connection import db
from src.database.db_operations import add_reminder

command_router = Router(name=__name__)


########################################
###          COMMAND HANDLERs        ###
########################################

@command_router.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.reply("Stay organized with me! Just drop a message in the chat and I will sort it out for you!")


@command_router.message(Command('list'))
async def send_list(message: types.Message):
    reminder_collection = db["reminders"]
    reminders = await reminder_collection.find().to_list(length=None)

    if not reminders:
        await message.answer("No tasks available.")
        return

    for reminder in reminders:
        await message.answer(f"{reminder}")

    # TODO: add menu after listing all the messages to choose whether user wants to manage them or not


@command_router.message(Command("manage"))
async def manage_menu(message: types.Message):
    reminder_collection = db["reminders"]
    reminders = await reminder_collection.find().to_list(length=None)

    # If no reminders exist, inform the user
    if not reminders:
        await message.answer("No tasks available.")
        return

    buttons = [
        [InlineKeyboardButton(text=f"Edit Task {reminder['name']}",
                              callback_data=f"edit_{reminder['_id']}")]
        for reminder in reminders
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer("Here are your tasks. Choose one to edit:", reply_markup=keyboard)


@command_router.callback_query(lambda c: c.data.startswith("edit_"))
async def edit_task(callback_query: types.CallbackQuery):
    print(callback_query.data)
    task_id = callback_query.data.split("_")[1]  # Extract task ID from the callback data
    print(task_id)
    # Fetch the task from the database using the task_id
    reminder_collection = db["reminders"]
    task = await reminder_collection.find_one({"_id": ObjectId(task_id)})

    if task:
        # Ask the user for new details for the task (e.g., new task name)
        await callback_query.message.answer(f"You selected: {task['name']}. Please enter the new task details:")
    else:
        await callback_query.message.answer("Task not found.")

    # Acknowledge the callback query
    await callback_query.answer()


# _____________________________________________________________________________

def create_menu(user_id, chat_id, message):
    # Create inline buttons
    buttons = [
        [InlineKeyboardButton(text="Low", callback_data=f"option_1,{user_id},{chat_id},{message}")],
        [InlineKeyboardButton(text="Medium", callback_data=f"option_2,{user_id},{chat_id},{message}")],
        [InlineKeyboardButton(text="High", callback_data=f"option_3,{user_id},{chat_id},{message}")]
    ]

    # Create the markup with the buttons
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard


@command_router.message(F.text)
async def handle_user_input(message: types.Message):
    user_input = message.text

    # Optionally store or process the user's input here
    print(f"User entered: {user_input}")

    user_input = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id

    # After user input, display the inline menu
    await message.answer("Choose one of the following priorities:",
                         reply_markup=create_menu(user_id, chat_id, user_input))


# Handle the user's selection from the menu
@command_router.callback_query(lambda c: c.data.startswith("option_"))
async def process_menu_selection(callback_query: types.CallbackQuery):
    selected_option, user_id, chat_id, task_message = callback_query.data.split(',')

    print(selected_option, user_id, chat_id, task_message)

    priority = 0
    # Process the user's selection
    if selected_option == "option_1":
        await callback_query.message.answer("You selected Low Priority")
        priority = 0
    elif selected_option == "option_2":
        await callback_query.message.answer("You selected Medium Priority")
        priority = 1
    elif selected_option == "option_3":
        await callback_query.message.answer("You selected High Priority")
        priority = 2

    # Remove the inline keyboard (menu)
    await callback_query.message.edit_reply_markup(reply_markup=None)

    # Acknowledge the user's selection and clear the inline buttons
    await callback_query.answer()

    # Uploads record to the collection into our DB
    await add_reminder(int(user_id), int(chat_id), task_message, int(priority))

    # Now the bot can continue to await further text input from the user
    await callback_query.message.answer("Your task was uploaded to the DB")
