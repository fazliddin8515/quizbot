from datetime import datetime

class Base: ...

class TimestampMixin:
    created_at: datetime
    updated_at: datetime

class User(Base, TimestampMixin):
    id: int
    first_name: str
    last_name: str | None
    username: str | None
    admins: list[Admin]

    def __init__(
        self,
        id: int,
        first_name: str,
        last_name: str | None = ...,
        username: str | None = ...,
    ) -> None: ...
    def __repr__(self) -> str: ...

class Channel(Base, TimestampMixin):
    id: int
    title: str
    username: str | None
    admins: list[Admin]
    quizzes: list[Quiz]

    def __init__(self, id: int, title: str, username: str | None = ...) -> None: ...
    def __repr__(self) -> str: ...

class Admin(Base, TimestampMixin):
    id: int
    user_id: int
    channel_id: int
    user: User
    channel: Channel

    def __init__(self, id: int, user_id: int, channel_id: int) -> None: ...
    def __repr__(self) -> str: ...

class Quiz(Base, TimestampMixin):
    id: int
    question: str
    correct: int
    channel_id: int
    channel: Channel
    options: list[Option]

    def __init__(
        self, id: int, question: str, correct: int, channel_id: int
    ) -> None: ...
    def __repr__(self) -> str: ...

class Option(Base, TimestampMixin):
    id: int
    option: str
    order: int
    quiz_id: int
    quiz: Quiz

    def __init__(self, id: int, option: str, order: int, quiz_id: int) -> None: ...
    def __repr__(self) -> str: ...
