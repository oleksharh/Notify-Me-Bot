from aiogram import types, Router, F
from aiogram.filters import Command
from src.database.db_operations import add_reminder, get_reminders, get_reminder_by_id
from src.utils.keyboards import create_edit_menu, create_priority_menu, create_manage_menu

command_router = Router(name=__name__)

########################################
###          COMMAND HANDLERS        ###
########################################

@command_router.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Stay organized with me! Just drop a message in the chat and I will sort it out for you!")

@command_router.message(Command("list"))
async def send_list(message: types.Message):
    reminders = await get_reminders()
    tasks = []

    if not reminders:
        await message.answer("No tasks available.")
        return

    for index, reminder in enumerate(reminders):
        task_object = {
            "task_id": index + 1,
            "task_message": reminder["message"],
            "priority": reminder["priority"],
        }
        tasks.append(task_object)

    tasks_str = "\n\n".join(
        [
            f"⚫️ Task ID: {task["task_id"]}\n"
            f"📝 Task: {task["task_message"]}\n"
            f"⭐️ Priority: {task["priority"]}\n"
            for task in tasks]
    )

    # await message.answer()
    keyboard = create_manage_menu()
    await message.answer(text="Your tasks are: \n\n" + tasks_str, reply_markup=keyboard)

@command_router.callback_query(lambda c: c.data.startswith("manage_"))
async def manage(callback_query: types.CallbackQuery):
    function = callback_query.data.split("_")[-1]

    if function == "manage":
        await manage_menu(callback_query.message) # TODO: Check what argument needs to be passed here
    else:
        await callback_query.message.edit_reply_markup(reply_markup=None)

    await callback_query.answer()


@command_router.message(Command("manage"))
async def manage_menu(message: types.Message):
    reminders = await get_reminders()

    if not reminders:
        await message.answer("No tasks available.")
        return

    keyboard = create_edit_menu(reminders)
    await message.answer("Here are your tasks. Choose one to edit:", reply_markup=keyboard)

@command_router.callback_query(lambda c: c.data.startswith("edit_"))
async def edit_task(callback_query: types.CallbackQuery):
    task_id = callback_query.data.split("_")[1]
    task = await get_reminder_by_id(task_id)

    if task:
        await callback_query.message.answer(f"You selected: {task["message"]}. Please enter the new task details:")
    else:
        await callback_query.message.answer("Task not found.")

    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer()


@command_router.message(F.text)
async def handle_user_input(message: types.Message):
    user_input = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id

    # After user input, display the inline menu
    await message.answer("Choose one of the following priorities:",
                         reply_markup=create_priority_menu(user_id, chat_id, user_input))

# Handle the user's selection from the menu
@command_router.callback_query(lambda c: c.data.startswith("option_"))
async def process_menu_selection(callback_query: types.CallbackQuery):
    selected_option, user_id, chat_id, task_message = callback_query.data.split(",")

    priority = {
        "option_1": 0,
        "option_2": 1,
        "option_3": 2
    }.get(selected_option, 0)

    # Uploads record to the collection into our DB
    await add_reminder(int(user_id), int(chat_id), task_message, int(priority))
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer()
    await callback_query.message.answer("Your task was uploaded to the DB")

