import json
from dataclasses import dataclass


@dataclass
class DataClass:
    presence: dict = None
    user_id: dict = None
    guild: dict = None
    role: dict = None
    channel: dict = None
    nhentai: dict = None
    url: dict = None

    def update(self):
        with open("./data/data.json", "r", encoding="utf8") as f:
            _data = json.load(f)
        self.presence = _data["presence"]
        self.user_id = _data["user_id"]
        self.guild = _data["guild"]
        self.role = _data["role"]
        self.channel = _data["channel"]
        self.nhentai = _data["nhentai"]
        self.url = _data["url"]
