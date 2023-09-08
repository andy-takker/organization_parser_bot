from aiogram_dialog import Dialog

from src.bot.windows.main_menu import MainMenuWindow


def get_dialog() -> Dialog:
    main_menu_window = MainMenuWindow()
    return Dialog(
        main_menu_window,
    )
