from aiogram import Router
from handlers.users import start


def setup_routers() -> Router:
    router = Router()
    router.include_router(start.router)
    return router
