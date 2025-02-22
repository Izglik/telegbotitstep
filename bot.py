import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from api import TOKEN

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

# Инлайн клавиатура
inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Начать", callback_data="start")],
        [InlineKeyboardButton(text="Помощь", callback_data="help")],
        [InlineKeyboardButton(text="Рандомное число", callback_data="random")]
    ]
)

@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    if callback.data == "start":
        await callback.message.answer("Нажмите /start, что бы начать работу с ботом")
    elif callback.data == "help":
        await callback.message.answer("Альтернативная помощь или нажми /help")
    elif callback.data == "random":
        await callback.message.answer("Хочешь рандомное число? Напиши /random")

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я тестовый бот <b>test</b>", reply_markup=main_keyboard)

@dp.message(lambda message: message.text == "Привет!")
async def hello(message: types.Message):
    await message.answer("Привет!!! Как дела?", reply_markup=inline_keyboard)

@dp.message(Command("random"))
async def random_command(message: types.Message):
    number = random.randint(1, 100)
    await message.answer(f"Случайное число: {number}")

@dp.message(Command("help"))
async def help_command(message: types.Message):
    command_text = (
        "Доступные команды\n"
        "/start - начать работу с ботом\n"
        "/help - Показывает список комманд\n"
        "/random - Генерирует рандомное число"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())