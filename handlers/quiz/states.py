from aiogram.dispatcher.filters.state import State, StatesGroup

class QuizState(StatesGroup):
    choosing_fan = State()
    choosing_baza = State()
    answering = State()
    message_ids = State()
    