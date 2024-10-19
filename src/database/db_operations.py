from .db_connection import db
from datetime import datetime
from bson import ObjectId


async def get_reminders(user_id: int, chat_id: int):
    reminder_collection = db["reminders"]
    return await reminder_collection.find({"user_id": user_id, "chat_id": chat_id}).to_list(length=None)


async def get_reminder_by_id(task_id):
    reminder_collection = db["reminders"]
    return await reminder_collection.find_one({"_id": ObjectId(task_id)})


async def add_reminder(user_id: int, chat_id: int, message: str, priority: int) -> str:
    reminder_collection = db["reminders"]

    new_record = {
        "user_id": user_id,
        "chat_id": chat_id,
        "message": message,
        "priority": priority,
        "timestamp": datetime.now()
    }

    # Insert the new task into the reminders collection
    result = await reminder_collection.insert_one(new_record)

    return str(result.inserted_id)
