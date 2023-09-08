import os
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: SecretStr = SecretStr("default")
    SQLITE_DB_PATH: Path = Path("./bot.sqlite3")

    def build_db_connection_uri(self) -> str:
        sqlite_path = os.fspath(self.SQLITE_DB_PATH)
        return f"sqlite+aiosqlite:///{sqlite_path}"
