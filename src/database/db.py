import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from src.config import MONGODB_URI, DATABASE_NAME
from bson import ObjectId
from datetime import datetime


class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.reminders_collection = None

    async def connect(self):
        self.client = AsyncIOMotorClient(MONGODB_URI, tlsCAFile=certifi.where())
        self.db = self.client[DATABASE_NAME]
        self.reminders_collection = self.db["reminders"]

    async def close(self):
        if self.client:
            self.client.close()

    #Operations

    async def get_all_reminders(self):
        return await self.reminders_collection.find().to_list(length=None)

    async def get_reminders(self, user_id: int, chat_id: int):
        return await self.reminders_collection.find({"user_id": user_id, "chat_id": chat_id}).to_list(length=None)

    async def get_reminder_by_id(self, task_id: str | ObjectId):
        return await self.reminders_collection.find_one({"_id": ObjectId(task_id)})

    async def add_reminder(self, user_id: int, chat_id: int, message: str, priority: int) -> str:
        new_record = {
            "user_id": user_id,
            "chat_id": chat_id,
            "message": message,
            "priority": priority,
            "status": False,
            "timestamp": datetime.now()
        }

        result = await self.reminders_collection.insert_one(new_record)

        return str(result.inserted_id)

    async def remove_reminder(self, task_id: str):
        await self.reminders_collection.delete_one({"_id": ObjectId(task_id)})
        return True

    async def update_task_status(self, task_id: str | ObjectId, status: bool):
        result = await self.reminders_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"status": status}}
        )

        if result.matched_count == 1:
            return True
        else:
            return False

