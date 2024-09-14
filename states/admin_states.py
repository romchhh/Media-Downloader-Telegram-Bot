from aiogram.dispatcher.filters.state import State, StatesGroup

    
class BroadcastState(StatesGroup):
    text = State()
    photo = State()
    button_name = State()
    button_url = State()
    preview = State()

