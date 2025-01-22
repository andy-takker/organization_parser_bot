from dataclasses import dataclass, field
from os import environ

import sentry_sdk
from sentry_sdk.integrations.asyncio import AsyncioIntegration


def setup_sentry(dsn: str) -> None:
    if not dsn:
        raise ValueError("APP_SENTRY_DSN is not set")
    sentry_sdk.init(
        dsn=dsn,
        traces_sample_rate=1.0,
        integrations=[AsyncioIntegration()],
    )


@dataclass(frozen=True, kw_only=True, slots=True)
class SentryConfig:
    dsn: str = field(default_factory=lambda: environ.get("APP_SENTRY_DSN", ""))
    use_sentry: bool = field(
        default_factory=lambda: environ.get("APP_SENTRY_USE", "false").lower() == "true"
    )
