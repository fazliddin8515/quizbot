from enum import Enum


class UserMemberStatus(str, Enum):
    OWNER = "creator"
    ADMIN = "administrator"
    MEMBER = "member"
    LEFT = "left"
    BANNED = "kicked"


class BotMemberStatus(str, Enum):
    ADMIN = "administrator"
    LEFT = "left"
    BANNED = "kicked"


class UserChangeType(str, Enum):
    BECAME_OWNER = "became_owner"
    BECAME_ADMIN = "became_admin"
    BECAME_MEMBER = "became_member"
    LEFT = "left"
    BANNED = "banned"


class BotChangeType(str, Enum):
    BECAME_ADMIN = "became_admin"
    LEFT = "left"
    BANNED = "banned"
