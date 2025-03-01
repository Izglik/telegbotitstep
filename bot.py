# Все нужные библиотеки
import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from api import TOKEN
from weather import get_weather
from films import Movies

# Создаем объект - бот и диспетчер
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Основная клавиатура
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привет!"), KeyboardButton(text="Помощь")]
    ],
    resize_keyboard=True
)

# Инлайн клавиатура/Добовляет кнопки и какую команду оно выполняет
inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Начать", callback_data="start")],
        [InlineKeyboardButton(text="Помощь", callback_data="help")],
        [InlineKeyboardButton(text="Рандомное число", callback_data="random")],
        [InlineKeyboardButton(text="Погода сегодня", callback_data="weather")]
    ]
)

# Что выводит когда мы нажимаем 
@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    if callback.data == "start":
        await start(callback.message)  # Вместо отправки текста вызываем команду /start
    elif callback.data == "help":
        await help_command(callback.message)  # Вызываем /help
    elif callback.data == "random":
        await random_command(callback.message)  # Вызываем /random
    elif callback.data == "weather":
        await weather_command(callback.message)  # Вызываем /weather

# Приветствует нас
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я тестовый бот <b>test</b>", reply_markup=main_keyboard)

# Просто здорвается и показывает кнопки
@dp.message(lambda message: message.text == "Привет!")
async def hello(message: types.Message):
    await message.answer("Привет!!! Как дела?", reply_markup=inline_keyboard)

# На комадну рандом выводит радномое число используя библиотеку random
@dp.message(Command("random"))
async def random_command(message: types.Message):
    number = random.randint(1, 100)
    await message.answer(f"Случайное число: {number}")

@dp.message(Command("film"))
async def film_command(message: types.Message):
    i = random.randint(1, 100)
    await message.answer(f"Случайный фильм: {Movies[i]}")

# На команду помошь даем доступные на этот момент команды
@dp.message(Command("help"))
async def help_command(message: types.Message):
    command_text = (
        "Доступные команды\n"
        "/start - начать работу с ботом\n"
        "/help - Показывает список команд\n"
        "/random - Генерирует рандомное число\n"
        "/weather - Показывает погоду в Алматы на данный момент"
    )
    await message.answer(command_text)  # Отправляем пользователю командный список


@dp.message(Command("weather"))
async def weather_command(message: types.Message):
    weather_info = await get_weather()  # Получаем информацию о погоде
    await message.answer(weather_info)  # Отправляем информацию о погоде


# Запускает бота
async def main():
    await dp.start_polling(bot)
    print("Бот запущен")

# Для выполнение всех команд одноврененно и всегда(наверное)
if __name__ == "__main__":
    asyncio.run(main())