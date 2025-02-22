import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode
from api import TOKEN  # из файла api добавляем token
from aiogram.client.default import DefaultBotProperties

# Создаем объект бот и диспетчер
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Основная клавиатура
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Привет"), KeyboardButton("Помощь")]
    ], resize_keyboard=True
)

# Инлайн клавиатура
inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Перейти на сайт", url="https://example.com")],
        [InlineKeyboardButton(text="Нажми", callback_data="button_click")]
    ]
)

# Проверка, работает ли команда /qwe
@dp.message(Command("qwe"))
async def send_welcome(message: Message):
    await message.answer("rty")


@dp.message(lambda message: message.text == "Привет!")
async def hello(message: type.Message):
    await message.answer("Привет!!! Как дела?", reply_markup=inline_keyboard)


@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Я твой <b>Telegram-бот</b> 🤖")


@dp.message(Command("help"))
async def send_welcome(message: Message):
    await message.answer("Я ничего пока не умею, только команды /start а так же /help")


async def main():
    print("Бот запущен")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
