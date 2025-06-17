import asyncio

from aiogram import types
from bot import bot
from db import get_session
from helpers import (
    ChangeType,
    MemberSource,
    add_channel_admins,
    del_channel_admins,
    detect_change,
    extract_status,
    upsert_channel,
)


async def start_handler(message: types.Message) -> None:
    await message.answer("Hello World!")


async def my_chat_member_handler(update: types.ChatMemberUpdated) -> None:
    old_status = extract_status(update, MemberSource.OLD)
    new_status = extract_status(update, MemberSource.NEW)
    change_type = detect_change(old_status, new_status)

    async for session in get_session():
        channel = await upsert_channel(session, update.chat)
        if change_type == ChangeType.ADDED:
            await asyncio.sleep(1)
            admin_members = await bot.get_chat_administrators(update.chat.id)
            await add_channel_admins(session, channel, admin_members)
        elif change_type == ChangeType.REMOVED:
            await del_channel_admins(session, channel)

        await session.commit()
