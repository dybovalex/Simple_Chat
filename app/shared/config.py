import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATABASE_PATH = PROJECT_ROOT / "instance" / "chat.db"
DATABASE_URI = f"sqlite:///{DATABASE_PATH}"

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
TIMEZONE = "Europe/Vienna"
