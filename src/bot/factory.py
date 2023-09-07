import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from src.bot.config import Settings
from src.bot.db.factory import create_engine, create_session_factory
from src.bot.dialogs import register_dialogs
from src.bot.middlewares.db import DatabaseMiddleware
from src.bot.middlewares.settings import SettingsMiddleware
from src.bot.ui_commands import set_ui_commands

logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    settings = Settings()
    if settings.TELEGRAM_BOT_TOKEN.get_secret_value() == "default":
        raise ValueError("You should set env TELEGRAM_BOT_TOKEN")
    engine = create_engine(connection_uri=settings.build_db_connection_uri())
    session_factory = create_session_factory(engine=engine)

    bot = create_bot(settings=settings)
    storage = create_storage(settings=settings)
    dp = Dispatcher(storage=storage)
    dp.update.outer_middleware(SettingsMiddleware(settings=settings))
    dp.update.outer_middleware(DatabaseMiddleware(session_factory=session_factory))
    register_dialogs(dp)
    setup_dialogs(dp)

    await set_ui_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    finally:
        await engine.dispose()
        logger.info("Stopped")


def create_bot(settings: Settings) -> Bot:
    return Bot(
        token=settings.TELEGRAM_BOT_TOKEN.get_secret_value(),
        parse_mode=ParseMode.HTML,
    )


def create_storage(settings: Settings) -> BaseStorage:
    return MemoryStorage()
