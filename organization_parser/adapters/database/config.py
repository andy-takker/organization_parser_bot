from dataclasses import dataclass, field
from os import environ


@dataclass(frozen=True, kw_only=True, slots=True)
class DatabaseConfig:
    dsn: str = field(default_factory=lambda: environ["APP_DATABASE_DSN"])

    pool_size: int = field(
        default_factory=lambda: int(environ.get("APP_DATABASE_POOL_SIZE", 20))
    )
    pool_timeout: int = field(
        default_factory=lambda: int(environ.get("APP_DATABASE_POOL_TIMEOUT", 5))
    )
    pool_max_overflow: int = field(
        default_factory=lambda: int(environ.get("APP_DATABASE_MAX_OVERFLOW", 5))
    )
