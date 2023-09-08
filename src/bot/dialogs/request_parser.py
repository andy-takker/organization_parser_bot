from aiogram_dialog import Dialog

from src.bot.states import RequestParserSG
from src.bot.windows.confirm import ConfirmWindow
from src.bot.windows.input_form_field import InputFormWindow


def get_dialog() -> Dialog:
    return Dialog(
        InputFormWindow(
            state=RequestParserSG.place,
            message="Введите место, где осуществить поиск?",
            field_name="place",
            is_first=True,
        ),
        InputFormWindow(
            state=RequestParserSG.query,
            message="Введите какие организации искать?\n(можно больше одного слова)",
            field_name="query",
        ),
        InputFormWindow(
            state=RequestParserSG.radius,
            message="Укажите радиус поиска в км\n(введите только число)",
            field_name="radius",
            type_factory=float,
        ),
        ConfirmWindow(state=RequestParserSG.confirm),
    )
