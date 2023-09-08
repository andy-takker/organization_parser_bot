from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from src.bot.db.provider import DatabaseProvider
from src.bot.states import MainMenuSG, RegistrationSG


async def start_command(
    message: Message,
    dialog_manager: DialogManager,
    provider: DatabaseProvider,
) -> None:
    if message.from_user is None:
        return
    user = await provider.user.get_by_id_or_none(message.from_user.id)
    if user is not None:
        await dialog_manager.start(MainMenuSG.main_menu, mode=StartMode.RESET_STACK)
    else:
        await message.answer(
            "Добро пожаловать! Чтобы начать делать выгрузки "
            "нужно зарегистрировать новый "
            '<a href="https://yandex.com/dev/maps/geosearch/">API ключ</a>'
        )
        await dialog_manager.start(
            RegistrationSG.set_api_key,
            mode=StartMode.RESET_STACK,
        )
