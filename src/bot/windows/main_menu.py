from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from src.bot.states import ChangeAPIKeySG, MainMenuSG, RequestParserSG


class MainMenuWindow(Window):
    def __init__(self) -> None:
        super().__init__(
            Const("Главное меню"),
            Start(
                text=Const("Новый запрос к API"),
                id="new_request",
                state=RequestParserSG.place,
            ),
            Start(
                text=Const("Заменить API ключ"),
                id="change_api_key",
                state=ChangeAPIKeySG.change_api_key,
            ),
            state=MainMenuSG.main_menu,
        )
