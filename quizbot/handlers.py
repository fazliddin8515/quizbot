from typing import Literal

from aiogram import types
from db import get_session
from models import Channel
from sqlalchemy import select


def check_status(
    update: types.ChatMemberUpdated, status: Literal["added", "removed"]
) -> bool:
    is_added = isinstance(
        update.old_chat_member, types.ChatMemberBanned | types.ChatMemberLeft
    ) and isinstance(update.new_chat_member, types.ChatMemberAdministrator)

    is_removed = isinstance(
        update.old_chat_member, types.ChatMemberAdministrator
    ) and isinstance(update.new_chat_member, types.ChatMemberBanned)

    return (status == "added" and is_added) or (status == "removed" and is_removed)


async def start_handler(message: types.Message) -> None:
    await message.answer("Hello World!")


async def my_chat_member_handler(update: types.ChatMemberUpdated) -> None:
    is_added = check_status(update, "added")
    is_removed = check_status(update, "removed")

    async for session in get_session():
        find_channel = select(Channel).where(Channel.id == update.chat.id)
        channel = await session.scalar(find_channel)
        if is_added and not channel:
            pass
        if is_removed and channel:
            pass
