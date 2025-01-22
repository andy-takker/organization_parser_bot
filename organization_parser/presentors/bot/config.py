from dataclasses import dataclass, field
from os import environ

from organization_parser.adapters.database.config import DatabaseConfig


@dataclass(frozen=True, slots=True, kw_only=True)
class TelegramBot:
    token = field(default_factory=lambda: environ["APP_TELEGRAM_BOT_TOKEN"])


@dataclass(frozen=True, slots=True, kw_only=True)
class BotConfig:
    db: DatabaseConfig = field(default_factory=DatabaseConfig)
