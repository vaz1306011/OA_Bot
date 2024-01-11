import json

with open("./data/data.json", "r", encoding="utf8") as f:
    _data: dict = json.load(f)

DATA: dict = _data
PRESENCE: dict = _data["presence"]
USER_ID: dict = _data["user_id"]
URL: dict = _data["url"]
