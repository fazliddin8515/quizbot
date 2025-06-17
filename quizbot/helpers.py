from enum import Enum
from typing import Literal

from aiogram import types
from models import Admin, Channel, User
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession


class MemberStatus(str, Enum):
    ADMIN = "administrator"
    KICKED = "kicked"
    LEFT = "left"


class MemberSource(str, Enum):
    OLD = "old"
    NEW = "new"


class ChangeType(str, Enum):
    ADDED = "added"
    REMOVED = "removed"
    NONE = "none"


def extract_status(
    update: types.ChatMemberUpdated, source: MemberSource
) -> MemberStatus:
    chat_member = (
        update.old_chat_member if source == MemberSource.OLD else update.new_chat_member
    )

    if isinstance(chat_member, types.ChatMemberAdministrator):
        return MemberStatus.ADMIN
    if isinstance(chat_member, types.ChatMemberBanned):
        return MemberStatus.KICKED
    if isinstance(chat_member, types.ChatMemberLeft):
        return MemberStatus.LEFT

    raise ValueError("Unknown chat member status")


def detect_change(old: MemberStatus, new: MemberStatus) -> ChangeType:
    if old in {MemberStatus.LEFT, MemberStatus.KICKED} and new == MemberStatus.ADMIN:
        return ChangeType.ADDED
    if old == MemberStatus.ADMIN and new in {MemberStatus.LEFT, MemberStatus.KICKED}:
        return ChangeType.REMOVED
    return ChangeType.NONE


async def upsert_channel(session: AsyncSession, chat: types.Chat) -> Channel:
    channel = await session.get(Channel, chat.id)
    if channel:
        channel.title = chat.title
        channel.username = chat.username
        return channel

    channel = Channel(id=chat.id, title=chat.title, username=chat.username)
    session.add(channel)
    return channel


async def upsert_user(
    session: AsyncSession, member: types.ResultChatMemberUnion
) -> User:
    user = await session.get(User, member.user.id)
    if user:
        user.first_name = member.user.first_name
        user.last_name = member.user.last_name
        user.username = member.user.username
    else:
        user = User(
            id=member.user.id,
            first_name=member.user.first_name,
            last_name=member.user.last_name,
            username=member.user.username,
        )
        session.add(user)

    return user


async def add_channel_admins(
    session: AsyncSession, channel: Channel, admins: list[types.ResultChatMemberUnion]
) -> None:
    for admin_member in admins:
        if not admin_member.user.is_bot:
            user = await upsert_user(session, admin_member)
            admin = Admin(user_id=user.id, channel_id=channel.id)
            session.add(admin)


async def del_channel_admins(session: AsyncSession, channel: Channel) -> None:
    stmt = delete(Admin).where(Admin.channel_id == channel.id)
    await session.execute(stmt)
