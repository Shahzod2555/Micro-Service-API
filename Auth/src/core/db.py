from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.config import settings
from src.core.models import Base


class Database:
    def __init__(self):
        self.engine = create_async_engine(url=settings.DB_URL)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session
            await session.commit()

    async def init_database(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


db_helper = Database()
