from dotenv import load_dotenv
import os

load_dotenv(".env.local")

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("No API token found. Please add your bot token to .env.local.")

DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")
if not DB_CONNECTION_STRING:
    raise ValueError("DB connection wasn't set, please check the status of your DB String")
