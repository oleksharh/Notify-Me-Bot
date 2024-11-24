from typing import List, Union
from datetime import time


class UserConfig:
    PRIORITY_TIMES = {
        "low": ['0 9 * * *'],  # Morning only
        "medium": ['0 9 * * *', '0 13 * * *'],  # Morning and afternoon
        "high": ['0 9 * * *', '0 13 * * *', '0 18 * * *'],  # Morning, afternoon, and evening
        "ultra": [f'0 {hour} * * *' for hour in range(9, 24)]  # Every hour from 9:00 to 23:00
    }

    def __init__(self, db):
        self.db = db
        self.user_configs = self.db["user_configs"]

    async def save_user_info(self, user_id: int, timezone: str):
        existing_preference = await self.user_configs.find_one({"user_id": user_id})

        if not existing_preference:
            result = await self.user_configs.insert_one({
                "user_id": user_id,
                "timezone": timezone,
                "custom_priority_times": {
                    "low": None,
                    "medium": None,
                    "high": None,
                    "ultra": None
                },
            })
            try:
                return result.inserted_id
            finally:
                return "Not Successful"

    async def update_user_configs(self, user_id: int, priority: str, reminder_time: int) -> str:
        """
        Save or update the user's preferred
        reminder time for a given priority
        """

        result = await self.user_configs.update_one(
            {"user_id": user_id},
            {"$set": {f"custom_priority_times.{priority}": reminder_time}},
            upsert=True
        )
        return str(result.upserted_id) if result.upserted_id else "Updated"

    async def get_user_configs(self, user_id: int) -> List[dict]:
        """
        Retrieve all reminder time
        preferences for the user
        """
        preference = await self.user_configs.find_one({"user_id": user_id})
        return preference or {}
