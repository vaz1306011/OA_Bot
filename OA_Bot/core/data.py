import json
from dataclasses import dataclass

from OA_Bot.core.paths import DATA_FILE


@dataclass
class DataClass:
    presence: dict = None
    user_id: dict = None
    guild: dict = None
    role: dict = None
    channel: dict = None
    url: dict = None

    def update(self):
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not DATA_FILE.exists():
            DATA_FILE.write_text(json.dumps({}), encoding="utf8")
        with DATA_FILE.open("r", encoding="utf8") as f:
            _data = json.load(f)
        self.presence = _data.get("presence", {})
        self.user_id = _data.get("user_id", {})
        self.guild = _data.get("guild", {})
        self.role = _data.get("role", {})
        self.channel = _data.get("channel", {})
        self.url = _data.get("url", {})
