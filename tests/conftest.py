from typing import AsyncGenerator

import fastapi
import pytest
from async_asgi_testclient import TestClient

from app import app


@pytest.fixture
async def test_app() -> fastapi.FastAPI:
    return app.create_app()


@pytest.fixture
async def client(test_app) -> AsyncGenerator[TestClient, None]:
    async with TestClient(test_app) as client:
        yield client
