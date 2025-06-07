from aiogram import Dispatcher, types
from aiogram.filters import CommandStart

dp = Dispatcher()


async def start_handler(message: types.Message) -> None:
    await message.answer("Hello World!")


dp.message.register(start_handler, CommandStart())
