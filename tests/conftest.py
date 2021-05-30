from typing import AsyncGenerator

import fastapi
import pytest
from app.app import Settings, create_app
from async_asgi_testclient import TestClient


@pytest.fixture
async def test_app() -> fastapi.FastAPI:
    settings = Settings(client_id="client_id")
    return create_app(settings)


@pytest.fixture
async def client(test_app) -> AsyncGenerator[TestClient, None]:
    async with TestClient(test_app) as client:
        yield client
