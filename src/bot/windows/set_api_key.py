from typing import Any

from aiogram.fsm.state import State
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const, Format

from src.bot.db.provider import DatabaseProvider
from src.bot.states import MainMenuSG
from src.core.service.utils import validate_api_key


class SetAPIKeyWindow(Window):
    def __init__(
        self,
        state: State,
        back_state: State | None = None,
    ) -> None:
        widgets = [Format("{message}"), MessageInput(func=handle_api_key)]
        if back_state is not None:
            widgets.append(Cancel(text=Const("Назад")))
        super().__init__(*widgets, state=state, getter=get_message_data)  # type: ignore[arg-type]


async def get_message_data(
    dialog_manager: DialogManager, **kwargs: dict[str, Any]
) -> dict[str, str]:
    user_id = dialog_manager.event.from_user.id  # type: ignore[union-attr]
    provider: DatabaseProvider = dialog_manager.middleware_data["provider"]
    user = await provider.user.get_by_id_or_none(user_id=user_id)
    message = "Введите API ключ"
    if user is not None:
        message = (
            f"Ваш текущий ключ: <b>{user.yandex_api_key}</b>\nОтправьте новый API ключ"
        )
    return {"message": message}


async def handle_api_key(
    m: Message, widget: MessageInput, manager: DialogManager
) -> None:
    if m.from_user is None:
        return
    if not validate_api_key(str(m.text)):
        await m.answer("Ключ некорректный")
        return
    provider: DatabaseProvider = manager.middleware_data["provider"]
    await provider.user.create_or_update(
        user_id=m.from_user.id, yandex_api_key=str(m.text)
    )
    await m.answer("Ключ сохранен")
    await manager.start(state=MainMenuSG.main_menu, mode=StartMode.RESET_STACK)
