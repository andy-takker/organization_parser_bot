from aiogram_dialog import Dialog

from src.bot.states import RegistrationSG
from src.bot.windows.set_api_key import SetAPIKeyWindow


def get_dialog() -> Dialog:
    return Dialog(
        SetAPIKeyWindow(state=RegistrationSG.set_api_key),
    )
