from enums import (
    BotChangeType,
    BotMemberStatus,
    UserChangeType,
    UserMemberStatus,
)

USER_STATUS_MAPPING: dict[UserMemberStatus, UserChangeType] = {
    UserMemberStatus.OWNER: UserChangeType.BECAME_OWNER,
    UserMemberStatus.ADMIN: UserChangeType.BECAME_ADMIN,
    UserMemberStatus.MEMBER: UserChangeType.BECAME_MEMBER,
    UserMemberStatus.LEFT: UserChangeType.LEFT,
    UserMemberStatus.BANNED: UserChangeType.BANNED,
}

BOT_STATUS_MAPPING: dict[BotMemberStatus, BotChangeType] = {
    BotMemberStatus.ADMIN: BotChangeType.BECAME_ADMIN,
    BotMemberStatus.LEFT: BotChangeType.LEFT,
    BotMemberStatus.BANNED: BotChangeType.BANNED,
}
