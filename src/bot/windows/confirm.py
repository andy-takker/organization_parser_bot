import asyncio
import logging
from textwrap import dedent
from typing import Any

from aiogram import Bot
from aiogram.fsm.state import State
from aiogram.types import BufferedInputFile, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, Window
from aiogram_dialog.widgets.kbd import Back, Button
from aiogram_dialog.widgets.text import Const, Format

from src.bot.db.provider import DatabaseProvider
from src.core.service.async_client import async_get_companies_dump
from src.core.service.utils import save_companies_to_buffered_excel_file

logger = logging.getLogger(__name__)


class ConfirmWindow(Window):
    message_template = dedent(
        """
    Место: {place}
    Запрос: {query}
    Радиус поиска: {radius} км
    """
    )

    def __init__(self, state: State) -> None:
        super().__init__(
            Format(self.message_template),
            Button(Const("Найти"), id="confirm", on_click=make_search_request),
            Back(Const("Назад")),
            getter=get_confirm_data,
            state=state,
        )


async def make_search_request(
    c: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    if c.bot is None:
        return
    provider: DatabaseProvider = manager.middleware_data["provider"]
    user = await provider.user._get_by_id(c.from_user.id)
    manager.show_mode = ShowMode.SEND
    asyncio.create_task(
        background_parse(
            bot=c.bot,
            user_id=c.from_user.id,
            api_key=user.yandex_api_key,
            place=manager.dialog_data["place"],
            query=manager.dialog_data["query"],
            radius_km=manager.dialog_data["radius"],
        )
    )
    await c.bot.send_message(
        text="Выполняю запрос на поиск. Ожидайте", chat_id=c.from_user.id
    )

    await manager.done()


async def get_confirm_data(
    dialog_manager: DialogManager,
    **kwargs: dict[str, Any],
) -> dict[str, Any | None]:
    return {
        "place": dialog_manager.dialog_data.get("place"),
        "query": dialog_manager.dialog_data.get("query"),
        "radius": dialog_manager.dialog_data.get("radius"),
    }


async def background_parse(
    bot: Bot, user_id: int, api_key: str, place: str, query: str, radius_km: float
) -> None:
    companies = await async_get_companies_dump(
        api_key=api_key,
        location=place,
        query=query,
        radius_km=radius_km,
    )
    if companies:
        excel_file = save_companies_to_buffered_excel_file(companies)
        await bot.send_document(
            document=BufferedInputFile(file=excel_file, filename="report.xlsx"),
            chat_id=user_id,
        )
    elif companies is None:
        await bot.send_message(
            chat_id=user_id,
            text="Произошла ошибка. Возможно закончился лимит у ключа на сегодня",
        )
    else:
        await bot.send_message(
            chat_id=user_id, text="Результат по вашему запросу не найден"
        )
    logger.info("background parse done!")
