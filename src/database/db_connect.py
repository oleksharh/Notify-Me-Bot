from src.database.db import Database

db = Database()

async def connect_db():
    await db.connect()

async def close_db():
    await db.close()