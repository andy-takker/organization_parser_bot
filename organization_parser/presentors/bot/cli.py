from organization_parser.application.logging import setup_logging
from organization_parser.presentors.bot.config import BotConfig


async def start(config: BotConfig) -> None:
    setup_logging()
