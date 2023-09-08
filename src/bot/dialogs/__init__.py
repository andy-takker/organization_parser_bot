from aiogram import F, Router
from aiogram.filters import Command

from src.bot.dialogs.change_api_key import get_dialog as get_change_api_key_dialog
from src.bot.dialogs.commands import start_command
from src.bot.dialogs.main_menu import get_dialog as get_main_menu_dialog
from src.bot.dialogs.registration import get_dialog as get_registration_dialog
from src.bot.dialogs.request_parser import get_dialog as get_request_parser_dialog
from src.bot.ui_commands import Commands


def register_dialogs(router: Router) -> None:
    dialog_router = Router()

    registration_dialog = get_registration_dialog()
    dialog_router.include_router(registration_dialog)

    main_menu_dialog = get_main_menu_dialog()
    dialog_router.include_router(main_menu_dialog)

    change_api_key_dialog = get_change_api_key_dialog()
    dialog_router.include_router(change_api_key_dialog)

    request_parser_dialog = get_request_parser_dialog()
    dialog_router.include_router(request_parser_dialog)

    dialog_router.message(Command(Commands.START))(start_command)

    router.message.filter(F.chat.type == "private")
    router.include_router(dialog_router)
