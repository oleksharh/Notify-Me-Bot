import aiocron
from aiogram import Bot
from src.database.db import Database
class ScheduledTasks:
    def __init__(self, db: Database, bot: Bot):
        self.db = db
        self.bot = bot
        self.setup_tasks()

    def setup_tasks(self):
        # Run every 10 seconds
        @aiocron.crontab('* * * * * */10')  # The extra * is for seconds
        async def ten_second_task():
            print(')')
            # reminders = await self.db.get_all_reminders()
            #
            # for reminder in reminders:
            #     print(reminder)