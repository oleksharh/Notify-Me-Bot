import aiocron
from aiogram import Bot
from src.database.db import Database


class ScheduledTasks:
    def __init__(self, db: Database, bot: Bot):
        self.db = db
        self.bot = bot
        self.setup_tasks()

    @staticmethod
    def setup_tasks():
        pass
