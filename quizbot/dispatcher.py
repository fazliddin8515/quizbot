from aiogram import Dispatcher
from aiogram.filters import CommandStart
from handlers import my_chat_member_handler, start_handler

dp = Dispatcher()


dp.message.register(start_handler, CommandStart())
dp.my_chat_member.register(my_chat_member_handler)
