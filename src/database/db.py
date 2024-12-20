import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Union, List
from src.config import MONGODB_URI, DATABASE_NAME, EXEMPT_USER_IDS, MAX_REMINDERS_PER_USER
from bson import ObjectId
from datetime import datetime
from src.database.user_config import UserConfig


# TODO: Add indexing on the most common attribute look up

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.reminders_collection = None
        self.user_config = None

    async def connect(self):
        self.client = AsyncIOMotorClient(MONGODB_URI, tls=True, tlsCAFile=certifi.where())
        self.db = self.client[DATABASE_NAME]
        self.reminders_collection = self.db["reminders"]
        self.user_config = UserConfig(self.db)

    async def close(self):
        if self.client:
            self.client.close()

    # Operations
    async def save_user_info(self, user_id: int, timezone: str):
        await self.user_config.save_user_info(user_id, timezone)

    async def update_user_configs(self, user_id: int, priority: str, reminder_time: int):
        await self.user_config.update_user_configs(user_id, priority, reminder_time)

    async def get_task_status(self, task_id: Union[ObjectId, str]) -> str:
        return await self.reminders_collection.find_one({"_id": ObjectId(task_id)})

    async def get_all_reminders(self):
        return await self.reminders_collection.find().to_list(length=None)

    async def get_reminders(self, user_id: int):
        # TODO: return only usable in the functions attributes instead of the full record
        return await self.reminders_collection.find({"user_id": user_id}).to_list(length=None)

    async def get_reminder_by_id(self, task_id: Union[str, ObjectId]):
        return await self.reminders_collection.find_one({"_id": ObjectId(task_id)})

    async def add_reminder(self, user_id: int, message: str, priority: Union[str, None]) -> str:
        record_count = await self.reminders_collection.count_documents({"user_id": user_id})
        print(record_count)
        if record_count > MAX_REMINDERS_PER_USER and user_id != EXEMPT_USER_IDS:
            return "limit"

        new_record = {
            "user_id": user_id,
            "message": message,
            "priority": priority,
            "is_finished": False,
            "timestamp": datetime.now()
        }

        result = await self.reminders_collection.insert_one(new_record)

        return str(result.inserted_id)

    async def remove_reminder(self, task_id: str):
        await self.reminders_collection.delete_one({"_id": ObjectId(task_id)})
        return True

    async def update_task_status(self, task_id: Union[str, ObjectId], status: bool) -> bool:
        result = await self.reminders_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"status": status}}
        )

        return self.check_if_updated(result)

    async def delete_task(self, task_id: Union[str, ObjectId]) -> bool:
        result = await self.reminders_collection.delete_one({"_id": ObjectId(task_id)})

        return self.check_if_updated(result)

    async def update_task_priority(self, task_id: Union[str, ObjectId], priority: str) -> bool:
        result = await self.reminders_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"priority": priority}}
        )

        return self.check_if_updated(result)


    @staticmethod
    def check_if_updated(result) -> bool:
        if result.matched_count == 1:
            return True
        else:
            return False
