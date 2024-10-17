from .db_connection import db  # Import the database instance
from datetime import datetime

async def add_reminder(user_id: int, chat_id: int, message: str, priority: int):
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
