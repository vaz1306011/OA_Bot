import json

with open("data.json", "r", encoding="utf8") as f:
    data = json.load(f)

DATA: dict = data
USER_ID: dict = data["user_id"]
ROLE: dict = data["role"]
CHANNEL: dict = data["channel"]
GUILD: dict = data["guild"]
URL: dict = data["url"]
