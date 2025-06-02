import asyncio

from aiogram import Bot, Dispatcher
from config.settings import settings
from routers import setup_routers

bot = Bot(token=settings.bot_token)
dp = Dispatcher()

async def main() -> None:
    dp.include_router(setup_routers())
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Botda xatolik yuz berdi {e}")