import os
from typing import AsyncGenerator

import fastapi
import pytest_asyncio

os.environ.setdefault("CLIENT_ID", "client_id")

from app.app import Settings, create_app  # noqa: E402
from async_asgi_testclient import TestClient  # noqa: E402


@pytest_asyncio.fixture
async def test_app() -> fastapi.FastAPI:
    settings = Settings(client_id="client_id")
    return create_app(settings)


@pytest_asyncio.fixture
async def client(test_app) -> AsyncGenerator[TestClient, None]:
    async with TestClient(test_app) as client:
        yield client
