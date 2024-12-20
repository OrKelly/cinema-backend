import asyncio
from collections.abc import Generator
from typing import Any
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from core.config import config
from core.database import (
    Base,
    reset_session_context,
    set_session_context,
)
from core.database.session import engines
from core.enums import RoleKindEnum
from core.security.jwt import JWTHandler
from core.server import create_app

from .factories.user import UserFactory
from .fixtures import *  # noqa: F403, I001


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)  # noqa: PT003
def session_context():
    session_id = str(uuid4())
    context = set_session_context(session_id=session_id)
    yield
    reset_session_context(context=context)


@pytest.fixture
async def prepare_database():
    assert config.MODE == "TEST"

    async with engines["writer"].begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")  # noqa: PT003
def app() -> Generator[FastAPI, Any, None]:
    app = create_app()
    yield app  # noqa:  PT022


@pytest.fixture(scope="function")  # noqa: PT003
async def client(app: FastAPI):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def logged_client(app: FastAPI):
    headers = {}
    user = await UserFactory().create()
    access_token = JWTHandler.encode({"user_id": user.id})
    headers["Authorization"] = f"Bearer {access_token}"
    async with AsyncClient(
        app=app, base_url="http://test", headers=headers
    ) as ac:
        yield ac


@pytest.fixture
async def admin_client(app: FastAPI):
    headers = {}
    user = await UserFactory(role=RoleKindEnum.ADMIN).create()
    access_token = JWTHandler.encode({"user_id": user.id})
    headers["Authorization"] = f"Bearer {access_token}"
    async with AsyncClient(
        app=app, base_url="http://test", headers=headers
    ) as ac:
        yield ac


@pytest.fixture
async def employee_client(app: FastAPI):
    headers = {}
    user = await UserFactory(role=RoleKindEnum.EMPLOYEE).create()
    access_token = JWTHandler.encode({"user_id": user.id})
    headers["Authorization"] = f"Bearer {access_token}"
    async with AsyncClient(
        app=app, base_url="http://test", headers=headers
    ) as ac:
        yield ac
