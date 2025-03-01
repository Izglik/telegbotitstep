# Все нужные библиотеки
import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from api import TOKEN
from weather import get_weather, get_available_cities
from FilmsBooks import Movies, Books

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
        [InlineKeyboardButton(text="Погода сегодня", callback_data="weather")],
        [InlineKeyboardButton(text="Фильм", callback_data="film")],
        [InlineKeyboardButton(text="Книга", callback_data="book")]
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
    elif callback.data == "film":
       await film_command(callback.message)
    elif callback.data == "book":
       await book_command(callback.message)
    

cities = get_available_cities()
@dp.message(lambda message: message.text in sum(cities.values(), []))
async def send_weather(message: types.Message):
    city = message.text
    weather_info = await get_weather(city)
    await message.answer(weather_info)

# Приветствует нас
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я тестовый бот <b>test</b>", reply_markup=main_keyboard)

# Просто здорвается и показывает кнопки
@dp.message(lambda message: message.text == "Кнопки")
async def hello(message: types.Message):
    await message.answer("Привет!!! Как дела?", reply_markup=inline_keyboard)

# На комадну рандом выводит радномое число используя библиотеку random
@dp.message(Command("random"))
async def random_command(message: types.Message):
    number = random.randint(1, 100)
    await message.answer(f"Случайное число: {number}")

@dp.message(Command("film"))
async def film_command(message: types.Message):
    f = random.randint(1, 100)
    await message.answer(f"Случайный фильм: {Movies[f]}")

@dp.message(Command("book"))
async def book_command(message: types.Message):
    b = random.randint(1, 100)
    await message.answer(f"Случайная книга: {Books[b]}")

# На команду помошь даем доступные на этот момент команды
@dp.message(Command("help"))
async def help_command(message: types.Message):
    command_text = (
        "Доступные команды\n"
        "/start - начать работу с ботом\n"
        "/help - Показывает список команд\n"
        "/random - Генерирует рандомное число\n"
        "/weather - Показывает погоду в Алматы на данный момент\n"
        "/film - Дает рандомный фильм\n"
        "/book - Дает рандомную книгу"
    )
    await message.answer(command_text)  # Отправляем пользователю командный список


@dp.message(Command("weather"))
async def weather_command(message: types.Message):
    weather_info = await get_weather()  # Получаем информацию о погоде
    await message.answer(weather_info)  # Отправляем информацию о погоде

@dp.message(lambda message: message.text == "Начать")
async def start_button(message: types.Message):
    await start(message)

@dp.message(lambda message: message.text == "Помощь")
async def help_button(message: types.Message):
    await help_command(message)

@dp.message(lambda message: message.text == "Рандомное число")
async def random_button(message: types.Message):
    await random_command(message)

@dp.message(lambda message: message.text == "Погода")
async def weather_button(message: types.Message):
    await weather_command(message)

# 📌 Клавиатуры для выбора города
cities = get_available_cities() # А зачем нам еще раз добовлять это? Где то сверху это уже есть

country_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇰🇿 Казахстан"), KeyboardButton(text="🇷🇺 Россия")]
    ],
    resize_keyboard=True
)

kazakhstan_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=city) for city in cities["Казахстан"]],
        [KeyboardButton(text="⬅ Назад")]
    ],
    resize_keyboard=True
)

russia_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=city) for city in cities["Россия"]],
        [KeyboardButton(text="⬅ Назад")]
    ],
    resize_keyboard=True
)

# 📌 Обработчик выбора страны
@dp.message(lambda message: message.text in ["🇰🇿 Казахстан", "🇷🇺 Россия"])
async def select_country(message: types.Message):
    if message.text == "🇰🇿 Казахстан":
        await message.answer("🏙 Выберите город в Казахстане:", reply_markup=kazakhstan_keyboard)
    elif message.text == "🇷🇺 Россия":
        await message.answer("🏙 Выберите город в России:", reply_markup=russia_keyboard)

# 📌 Обработчик выбора города
@dp.message(lambda message: message.text in sum(cities.values(), []))
async def select_city(message: types.Message):
    city = message.text
    weather_info = await get_weather(city)
    await message.answer(weather_info, reply_markup=country_keyboard)

# 📌 Обработчик кнопки "⬅ Назад"
@dp.message(lambda message: message.text == "⬅ Назад")
async def go_back(message: types.Message):
    await message.answer("🔙 Выберите страну:", reply_markup=country_keyboard)



# Запускает бота(Наверное)
async def main():
    await dp.start_polling(bot)

# Для выполнение всех команд одноврененно и всегда(наверное)
if __name__ == "__main__":
    asyncio.run(main())
