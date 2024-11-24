from aiogram import types, Router, F
from aiogram.filters import Command
from bson import ObjectId
from typing import Union
from src.database.db_connect import db
from src.utils.keyboards import MenuCreator


# TODO: generalize these status_manage_menu, delete_task_request_menu, priority_manage_menu into one callback_function
# TODO: add error handling, especially in get_reminders, update_task_status, add_reminder


priority_map = {"low": 0, "medium": 1, "high": 2, "ultra": 3}
priority_map_reverse = {0: "low", 1: "medium", 2: "high", 3: "ultra"}
priority_map_words = {0: "Morning", 1: "Afternoon", 2: "Evening", 3: "Ultra"}

menu_creator = MenuCreator()
command_router = Router(name="command_router")


# Welcome command handler function
@command_router.message(Command("start"))
async def send_welcome(message: types.Message) -> None:
    keyboard = menu_creator.user_config_options(message.from_user.id)

    print(message.date, type(message.date))

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

    await db.save_user_info(int(user_id),"timezone")

    if option == "default":
        await db.save_user_info(user_id, "timezone") # TODO ADD IMPLEMENTATION OF GETTING TIMEZONE FROM USER
        await callback_query.message.answer("You are all set, stay organized with me!")
        return

    keyboard = menu_creator.dayparts()
    await callback_query.message.answer("Choose part of the day you would like to edit", reply_markup=keyboard)


@command_router.callback_query(lambda c: c.data.startswith("daypart_"))
async def daypart_handler(callback_query: types.CallbackQuery):
    daypart = callback_query.data.split("_")[-1]

    await callback_query.message.delete()

    if daypart == "exit":
        await callback_query.message.answer("You are back in the main menu! \n"
                                            "POP in your message and we will sort it out for you")
        return

    daypart = int(daypart)

    daypart_map = {0: (0, 12), 1: (12, 18), 2: (18, 24), 3: "SPECIAL CASE"}
    daypart_words = {0: "morning", 1: "afternoon", 2: "evening", 3: "SPECIAL CASE"}

    start, end = daypart_map[daypart]
    keyboard = menu_creator.times_config(start, end, daypart)
    await callback_query.message.answer(f"Choose time for the {daypart_words[daypart]}", reply_markup=keyboard)


@command_router.callback_query(lambda c: c.data.startswith("times_config_"))
async def get_user_preferences(callback_query: types.CallbackQuery):
    _, _, hour, daypart = callback_query.data.split("_")
    hour = int(hour)
    daypart = int(daypart)
    user_id = callback_query.from_user.id

    await callback_query.message.delete()

    print(hour, daypart, user_id)

    await db.update_user_configs(user_id, priority_map_reverse[daypart], hour)

    keyboard = menu_creator.dayparts()
    await callback_query.message.answer(f"Your time for {priority_map_words[daypart].lower()} was updated")
    await callback_query.message.answer("Choose part of the day you would like to edit", reply_markup=keyboard)

    # TODO: fix the function above, update update_user_preferences method to process hours in the way of
    # deriving time from previous attributes, record and refine its structure in the collection for the optimized querying



# List All Tasks Command Handler
@command_router.message(Command("list"))
async def send_list(message: types.Message) -> None:
    user_id = message.from_user.id

    reminders = await db.get_reminders(user_id)

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
        f"⭐️ Priority: {reminder['priority']}\n"
        for index, reminder in enumerate(reminders)
    ]
    return "\n\n".join(tasks)


# Manage Tasks Callback Query Handler
@command_router.callback_query(lambda c: c.data.startswith("list_"))
async def list_manage(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    function = callback_query.data.split("_")[-1]

    # Remove inline keyboard after selection
    await callback_query.message.edit_reply_markup(reply_markup=None)

    if function == "manage":
        await manage_menu(callback_query.message, user_id)
    else:
        await callback_query.message.answer("You are back in the main menu!\n"
                                            "Please enter your next task.")

    await callback_query.answer()


# Manage Menu Command Handler
@command_router.message(Command("manage"))
async def manage_menu(message: types.Message, user_id=0):
    if user_id == 0:
        user_id = message.from_user.id

    reminders = await db.get_reminders(user_id)

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
    priority = callback_query.data.split("_")[1]
    task_id = callback_query.data.split("_")[2]

    await callback_query.message.delete()

    # await callback_query.message.answer(task_id, priority=priority) for DEBUGGING
    result = await db.update_task_priority(task_id, priority)
    if result:
        await callback_query.message.answer(f"Task priority updated to {priority}\n"
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


    inserted_id = await db.add_reminder(user_id, user_input, None)
    print(type(inserted_id))

    if inserted_id == "limit":
        await message.answer("Sorry your limit is up, we are not capable of saving more stuff"
                             " from you at the moment, as we use free hosting services with limited capacity")
        return

    # TODO: store the info above immediately without passing to the callback data,
    # and then in list functions strip off to 64bit size to fit inline buttons
    # and check for all possible mistakes with inserting info to the db
    # and passing less params in callback data

    # After user input, display the inline menu
    await message.answer("Choose one of the following priorities:",
                         reply_markup=menu_creator.priority_menu(inserted_id))


# Handle Priority Menu Selection
@command_router.callback_query(lambda c: c.data.startswith("option_"))
async def process_menu_selection(callback_query: types.CallbackQuery):
    priority, object_id = callback_query.data.split(",")

    priority = priority.split("_")[-1]

    # Remove the message after it's been handled
    await callback_query.message.delete()

    print(priority)

    # Upload task to the database
    await db.update_task_priority(object_id, priority)

    await callback_query.answer()
    await callback_query.message.answer("Your task was uploaded to the DB")
