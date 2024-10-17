from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bson import ObjectId

from src.database.db_connection import db

command_router = Router(name=__name__)


def create_menu():
    # Create inline buttons
    buttons = [
        [InlineKeyboardButton(text="Low", callback_data="option_1")],
        [InlineKeyboardButton(text="Medium", callback_data="option_2")],
        [InlineKeyboardButton(text="High", callback_data="option_3")]
    ]

    # Create the markup with the buttons
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard


########################################
###          COMMAND HANDLERs        ###
########################################

@command_router.message(Command('start'))
async def send_welcome(message: types.Message):
    reminder_collection = db["reminders"]
    reminders = await reminder_collection.find().to_list(length=None)

    print(reminders)

    for reminder in reminders:
        print(type(reminder))
        await message.reply(f"Hello! Welcome to the bot. Here are your reminders: {reminder}")

    await message.answer("Please enter your task:")


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

@command_router.message(F.text)
async def handle_user_input(message: types.Message):
    user_input = message.text

    # Optionally store or process the user's input here
    print(f"User entered: {user_input}")

    # After user input, display the inline menu
    await message.answer("Choose one of the following priorities:", reply_markup=create_menu())


# Handle the user's selection from the menu
@command_router.callback_query(lambda c: c.data.startswith("option_"))
async def process_menu_selection(callback_query: types.CallbackQuery):
    selected_option = callback_query.data

    # Process the user's selection
    if selected_option == "option_1":
        await callback_query.message.answer("You selected Low Priority")
        # Add record to the database
    elif selected_option == "option_2":
        await callback_query.message.answer("You selected Medium Priority")
        # Add record to the database
    elif selected_option == "option_3":
        await callback_query.message.answer("You selected High Priority")
        # Add record to the database

    # Remove the inline keyboard (menu)
    await callback_query.message.edit_reply_markup(reply_markup=None)

    # Acknowledge the user's selection and clear the inline buttons
    await callback_query.answer()

    # Now the bot can continue to await further text input from the user
    await callback_query.message.answer("Your task was uploaded to the DB")
