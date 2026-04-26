import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataClass:
    presence: dict = None
    user_id: dict = None
    guild: dict = None
    role: dict = None
    channel: dict = None
    url: dict = None

    def update(self):
        file_path = Path("./data/data.json")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if not file_path.exists():
            file_path.write_text(json.dumps({}), encoding="utf8")
        with open("./data/data.json", "r", encoding="utf8") as f:
            _data = json.load(f)
        self.presence = _data.get("presence", {})
        self.user_id = _data.get("user_id", {})
        self.guild = _data.get("guild", {})
        self.role = _data.get("role", {})
        self.channel = _data.get("channel", {})
        self.url = _data.get("url", {})
