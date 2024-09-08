from aiogram import Dispatcher, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from states import Form, RegistrationState
from calculator import CalorieCalculator
from products import get_buying_list
from crud_functions import is_included, add_user
from calories_db import initiate_calories_db

def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, CommandStart())
    dp.message.register(start_calories_calculation, F.text == "Рассчитать норму калорий")
    dp.callback_query.register(set_age_callback, F.data.in_({"female", "male"}))
    dp.message.register(process_age, F.text, Form.age)
    dp.message.register(process_growth, F.text, Form.growth)
    dp.message.register(process_weight, F.text, Form.weight)
    dp.message.register(get_formulas, F.text == "Формулы расчёта")
    dp.message.register(show_info, F.text == "Информация")
    dp.message.register(get_buying_list, F.text == "Купить")
    dp.callback_query.register(send_confirm_message, F.data.startswith("buy_"))
    dp.message.register(sign_up, F.text == "Регистрация")
    dp.message.register(set_username, F.text, RegistrationState.username)
    dp.message.register(set_email, F.text, RegistrationState.email)
    dp.message.register(set_age, F.text, RegistrationState.age)
    dp.message.register(handle_message)

async def cmd_start(message: Message):
    main_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Рассчитать норму калорий")],
            [KeyboardButton(text="Формулы расчёта")],
            [KeyboardButton(text="Информация")],
            [KeyboardButton(text="Купить")],
            [KeyboardButton(text="Регистрация")]
        ],
        resize_keyboard=True
    )
    await message.answer("Добро пожаловать! Выберите действие:", reply_markup=main_keyboard)

async def start_calories_calculation(message: Message, state: FSMContext):
    calculator = CalorieCalculator(state)
    await calculator.set_gender(message)

async def set_age_callback(call: CallbackQuery, state: FSMContext):
    calculator = CalorieCalculator(state)
    await state.update_data(gender=call.data)  # Сохраняем пол в состояние
    await calculator.set_age(call)

async def process_age(message: Message, state: FSMContext):
    calculator = CalorieCalculator(state)
    await calculator.process_numeric_input(message, 'age', "Теперь введите ваш рост:", Form.growth)

async def process_growth(message: Message, state: FSMContext):
    calculator = CalorieCalculator(state)
    await calculator.process_numeric_input(message, 'growth', "Теперь введите ваш вес:", Form.weight)

async def process_weight(message: Message, state: FSMContext):
    calculator = CalorieCalculator(state)
    await calculator.process_numeric_input(message, 'weight', "Спасибо за информацию! Идет расчет калорий...", None, lambda: calculator.calculate_calories(message))

async def get_formulas(message: Message):
    formula_women = "Формула Миффлина-Сан Жеора для женщин:\n" \
                    "10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) - 161"
    formula_men = "Формула Миффлина-Сан Жеора для мужчин:\n" \
                  "10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) + 5"
    await message.answer(f"{formula_women}\n\n{formula_men}")

async def show_info(message: Message):
    await message.answer("Этот бот помогает рассчитать ваши ежедневные потребности в калориях.")

async def send_confirm_message(call: CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

async def sign_up(message: Message, state: FSMContext):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await state.set_state(RegistrationState.username)

async def set_username(message: Message, state: FSMContext):
    username = message.text
    if is_included(username):
        await message.answer("Пользователь существует, введите другое имя:")
        await state.set_state(RegistrationState.username)
    else:
        await state.update_data(username=username)
        await message.answer("Введите свой email:")
        await state.set_state(RegistrationState.email)

async def set_email(message: Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    await message.answer("Введите свой возраст:")
    await state.set_state(RegistrationState.age)

async def set_age(message: Message, state: FSMContext):
    age = int(message.text)
    data = await state.get_data()
    username = data['username']
    email = data['email']
    add_user(username, email, age)
    await message.answer("Регистрация завершена!")
    await state.set_state(None)  # Завершение состояния

async def handle_message(message: Message):
    await message.answer('Привет! Я бот, который поможет тебе рассчитать норму калорий. \nИспользуй команду /start, чтобы начать.')