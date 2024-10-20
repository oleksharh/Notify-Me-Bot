import certifi
import motor.motor_asyncio
from ..config import DB_CONNECTION_STRING

client = motor.motor_asyncio.AsyncIOMotorClient(DB_CONNECTION_STRING, tlsCAFile=certifi.where())

db = client["notify-me-db"]

__all__ = ["db"]