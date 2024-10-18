import certifi
import motor.motor_asyncio
from dotenv import load_dotenv
import os

load_dotenv(".env.local")

DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")

if DB_CONNECTION_STRING is None:
    raise ValueError("No MongoDB connection string found in environment variables")

client = motor.motor_asyncio.AsyncIOMotorClient(DB_CONNECTION_STRING, tlsCAFile=certifi.where())

db = client["notify-me-db"]