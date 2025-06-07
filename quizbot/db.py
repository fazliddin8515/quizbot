import os
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

postgres_url: str = os.environ["POSTGRES_URL"]

engine = create_async_engine(postgres_url)

AsyncSessionLocal = async_sessionmaker(engine)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session
