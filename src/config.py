from dotenv import load_dotenv
import os

load_dotenv(".env.local")

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("No API token found. Please add your bot token to .env.local.")