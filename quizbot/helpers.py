from aiogram import types
from constants import BOT_STATUS_MAPPING, USER_STATUS_MAPPING
from enums import (
    BotChangeType,
    BotMemberStatus,
    UserChangeType,
    UserMemberStatus,
)
from models import Admin, Channel, User
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession


def extract_user_new_status(update: types.ChatMemberUpdated) -> UserMemberStatus:
    match update.new_chat_member:
        case types.ChatMemberOwner():
            return UserMemberStatus.OWNER
        case types.ChatMemberAdministrator():
            return UserMemberStatus.ADMIN
        case types.ChatMemberMember():
            return UserMemberStatus.MEMBER
        case types.ChatMemberLeft():
            return UserMemberStatus.LEFT
        case types.ChatMemberBanned():
            return UserMemberStatus.BANNED
        case _:
            raise ValueError(
                f"Unknown chat member type: {type(update.new_chat_member)}"
            )


def extract_bot_new_status(update: types.ChatMemberUpdated) -> BotMemberStatus:
    match update.new_chat_member:
        case types.ChatMemberAdministrator():
            return BotMemberStatus.ADMIN
        case types.ChatMemberLeft():
            return BotMemberStatus.LEFT
        case types.ChatMemberBanned():
            return BotMemberStatus.BANNED
        case _:
            raise ValueError(f"Unknown bot member type: {type(update.new_chat_member)}")


def detect_user_change(new_status: UserMemberStatus) -> UserChangeType:
    return USER_STATUS_MAPPING[new_status]


def detect_bot_change(new_status: BotMemberStatus) -> BotChangeType:
    return BOT_STATUS_MAPPING[new_status]


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
    new_admins = []
    for admin_member in admins:
        if not admin_member.user.is_bot:
            user = await upsert_user(session, admin_member)
            new_admin = Admin(user_id=user.id, channel_id=channel.id)
            new_admins.append(new_admin)
    session.add_all(new_admins)


async def delete_channel_admins(session: AsyncSession, channel: Channel) -> None:
    stmt = delete(Admin).where(Admin.channel_id == channel.id)
    await session.execute(stmt)
