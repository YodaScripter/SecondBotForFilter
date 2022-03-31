from aiogram.dispatcher.filters.state import State, StatesGroup


class MainLogic(StatesGroup):
    ShowMessage = State()
    EditType = State()
    EndShow = State()