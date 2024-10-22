from .db_connection import db
from datetime import datetime
from bson import ObjectId

reminder_collection = db["reminders"]

async def get_reminders(user_id: int, chat_id: int):
    return await reminder_collection.find({"user_id": user_id, "chat_id": chat_id}).to_list(length=None)


async def get_reminder_by_id(task_id):
    return await reminder_collection.find_one({"_id": ObjectId(task_id)})


async def add_reminder(user_id: int, chat_id: int, message: str, priority: int) -> str:
    new_record = {
        "user_id": user_id,
        "chat_id": chat_id,
        "message": message,
        "priority": priority,
        "status": False,
        "timestamp": datetime.now()
    }

    # Insert the new task into the reminders collection
    result = await reminder_collection.insert_one(new_record)

    return str(result.inserted_id)


async def remove_reminder(task_id: str):
    await reminder_collection.delete_one({"_id": ObjectId(task_id)})
    return True


async def update_task_status(task_id: str | ObjectId, status: bool):
    result = await reminder_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {"status": status}}
    )

    if result.matched_count == 1:
        return True  # Successfully updated
    else:
        return False  # Task not found or update failed
