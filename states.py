from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    gender = State()
    age = State()
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()