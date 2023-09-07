from textwrap import dedent
from typing import Any

from aiogram.fsm.state import State
from aiogram.types import BufferedInputFile, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, Window
from aiogram_dialog.widgets.kbd import Back, Button
from aiogram_dialog.widgets.text import Const, Format

from src.bot.db.provider import DatabaseProvider
from src.core.service.async_client import async_get_companies_dump
from src.core.service.utils import save_companies_to_buffered_csv_file


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
    companies = await async_get_companies_dump(
        api_key=user.yandex_api_key,
        location=manager.dialog_data.get("place", ""),
        query=manager.dialog_data.get("query", ""),
        radius_km=manager.dialog_data.get("radius", ""),
    )
    manager.show_mode = ShowMode.SEND
    if companies:
        csv_file = save_companies_to_buffered_csv_file(companies)
        await c.bot.send_document(
            document=BufferedInputFile(file=csv_file, filename="report.csv"),
            chat_id=c.from_user.id,
        )
    elif companies is None:
        await c.bot.send_message(
            chat_id=c.from_user.id,
            text="Произошла ошибка. Возможно закончился лимит у ключа на сегодня",
        )
    else:
        await c.answer(text="Результат по вашему запросу не найден")

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
