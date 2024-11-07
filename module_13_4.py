from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio

api = "Ключ для подключения к телеграмм боту"
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text = ['Colories'])
async def set_age(message):
    await message.answer("Введите свой возраст в годах")
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer("Введите свой рост в сантиметрах")
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer("Введите свой вес в килограммах")
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_colories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    calorie_allowance_man = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    calorie_allowance_woman = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161

    await message.answer(f"Ваша суточная норма калорий: для мужчин - {calorie_allowance_man} килокалорий,"
                         f" для женщин - {calorie_allowance_woman} килокалорий")
    await state.finish()

@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.')

@dp.message_handler()
async def all_messages(message):
    await message.answer("Введите команду /start, чтобы начать общение")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)
