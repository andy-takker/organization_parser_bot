import asyncio

from organization_parser.presentors.bot.cli import start
from organization_parser.presentors.bot.config import BotConfig

if __name__ == "__main__":
    config = BotConfig()
    asyncio.run(start(config=config))
