from aiogram_dialog import Dialog

from src.bot.states import ChangeAPIKeySG, MainMenuSG
from src.bot.windows.set_api_key import SetAPIKeyWindow


def get_dialog() -> Dialog:
    return Dialog(
        SetAPIKeyWindow(
            state=ChangeAPIKeySG.change_api_key, back_state=MainMenuSG.main_menu
        )
    )
