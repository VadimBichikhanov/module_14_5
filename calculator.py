from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from states import Form
from calories_db import add_calories_data

class CalorieCalculator:
    def __init__(self, state: FSMContext):
        self.state = state

    async def set_gender(self, message: Message):
        await message.answer("Выберите ваш пол:", reply_markup=self.get_gender_keyboard())
        await self.state.set_state(Form.gender)


    def get_gender_keyboard(self):
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Мужской", callback_data="male")],
                [InlineKeyboardButton(text="Женский", callback_data="female")]
            ]
        )

    async def set_age(self, call: CallbackQuery):
        await call.message.answer("Введите ваш возраст:")
        await self.state.set_state(Form.age)

    async def process_numeric_input(self, message: Message, field: str, prompt: str, next_state, callback=None):
        try:
            value = int(message.text)
            await self.state.update_data(**{field: value})
            if next_state:
                await message.answer(prompt)
                await self.state.set_state(next_state)
            elif callback:
                await callback()
        except ValueError:
            await message.answer("Пожалуйста, введите число.")

    async def calculate_calories(self, message: Message):
        data = await self.state.get_data()
        gender = data.get('gender')  # Используем get для безопасного доступа к ключу
        age = data['age']
        growth = data['growth']
        weight = data['weight']

        if not gender:
            await message.answer("Пол не был выбран. Пожалуйста, начните снова.")
            return

        if gender == 'female':
            calories = 10 * weight + 6.25 * growth - 5 * age - 161
        else:
            calories = 10 * weight + 6.25 * growth - 5 * age + 5

        await self.state.update_data(calories=calories)
        await self.state.set_state(None)

        # Сохранение данных о калориях в базу данных
        user_id = message.from_user.id
        add_calories_data(user_id, gender, age, growth, weight, calories)

        await message.answer(f"Ваша суточная норма калорий: {calories} ккал.")
