from typing import List, Union
from datetime import time


class UserConfig:
    PRIORITY_TIMES = {
        0: ['0 9 * * *'],  # Morning only
        1: ['0 9 * * *', '0 13 * * *'],  # Morning and afternoon
        2: ['0 9 * * *', '0 13 * * *', '0 18 * * *'],  # Morning, afternoon, and evening
        3: [f'0 {hour} * * *' for hour in range(9, 24)]  # Every hour from 9:00 to 23:00
    }

    def __init__(self, db):
        self.db = db
        self.preferences_collection = self.db["user_preferences"]

    async def save_user_info(self, user_id: int):
        existing_preference = await self.preferences_collection.find_one({"user_id": user_id})

        if not existing_preference:
            for priority, reminder_time in self.PRIORITY_TIMES.items():
                result = await self.preferences_collection.insert_one({
                    "user_id": user_id,
                    "priority": priority,
                    "reminder_times": reminder_time,
                })

    async def update_user_preference(self, user_id: int, priority: int, reminder_time: List[list]) -> str:
        """
        Save or update the user's preferred
        reminder time for a given priority
        """

        result = await self.preferences_collection.update_one(
            {"user_id": user_id},
            {"$set": {"priority": priority, "reminder_times": reminder_time}},
            upsert=True
        )
        return str(result.upserted_id) if result.upserted_id else "Updated"

    async def get_user_preferences(self, user_id: int) -> List[dict]:
        """
        Retrieve all reminder time
        preferences for the user
        """
        preference = await self.preferences_collection.find_one({"user_id": user_id})
        return preference or {}
