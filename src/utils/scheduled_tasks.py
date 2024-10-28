import aiocron
from aiogram import Bot
from src.database.db import Database


class ScheduledTasks:
    def __init__(self, db: Database, bot: Bot):
        self.db = db
        self.bot = bot
        self.setup_tasks()

    def setup_tasks(self):
        # Send all priority levels at 10:00
        @aiocron.crontab('0 10 * * *')
        async def task_10():
            await self.send_reminders([0, 1, 2])

        # Send priority 1 and 2 at 15:00
        @aiocron.crontab('0 15 * * *')
        async def task_15():
            await self.send_reminders([1, 2])

        # Send priority 2 only at 20:00
        @aiocron.crontab('0 20 * * *')
        async def task_20():
            await self.send_reminders([2])

    async def send_reminders(self, priorities):
        reminders = await self.db.get_all_reminders()

        filtered_reminders = [
            reminder for reminder in reminders
            if reminder['status'] is False and reminder['priority'] in priorities
        ]

        for reminder in filtered_reminders:
            try:
                await self.bot.send_message(
                    chat_id=reminder['chat_id'],
                    text=f"Reminder: {reminder['message']}"
                )
            except Exception as e:
                print(f"Failed to send reminder to chat_id {reminder['chat_id']}: {e}")
