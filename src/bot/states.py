from aiogram.fsm.state import State, StatesGroup


class RegistrationSG(StatesGroup):
    set_api_key = State()


class MainMenuSG(StatesGroup):
    main_menu = State()


class ChangeAPIKeySG(StatesGroup):
    change_api_key = State()


class RequestParserSG(StatesGroup):
    place = State()
    query = State()
    radius = State()
    confirm = State()
