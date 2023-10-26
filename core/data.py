import json

with open("data.json", "r", encoding="utf8") as f:
    _data: dict = json.load(f)

DATA: dict = _data
PRESENCE: dict = _data["presence"]
USER_ID: dict = _data["user_id"]
ROLE: dict = _data["role"]
CHANNEL: dict = _data["channel"]
GUILD: dict = _data["guild"]
URL: dict = _data["url"]
