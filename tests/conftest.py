import asyncio

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import config
from core.database import transactional
from core.database.session import Base

from .fixtures import *  # noqa: F403, I001


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncSession:
    async_engine = create_async_engine(config.TEST_DATABASE_URL)
    session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with session() as s:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        transactional.session = s
        yield s

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await async_engine.dispose()
