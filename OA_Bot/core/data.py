import json

from pydantic import BaseModel

from OA_Bot.core.logger import logger
from OA_Bot.core.paths import DATA_FILE


class DataClass(BaseModel):
    presence: dict = {}
    user_id: dict = {}
    guild: dict = {}
    role: dict = {}
    channel: dict = {}
    url: dict = {}

    @classmethod
    def load(cls) -> "DataClass":
        try:
            content = DATA_FILE.read_text(encoding="utf8")
            return cls.model_validate_json(content)
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            logger.error(f"無法解析{DATA_FILE}，請確保它是有效的 JSON 格式")
            return cls()

    def save(self):
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with DATA_FILE.open("w", encoding="utf8") as f:
            json.dump(self.model_dump(), f, ensure_ascii=False, indent=4)
        logger.info(f"已儲存機器人狀態到{DATA_FILE}")
