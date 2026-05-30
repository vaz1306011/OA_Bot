from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PACKAGE_DIR / "data"
DATA_FILE = DATA_DIR / "data.json"
ON_MESSAGE_IGNORE_DB = DATA_DIR / "on_message_ignore.db"
