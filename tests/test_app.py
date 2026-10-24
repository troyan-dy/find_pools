from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_request(client):
    response = await client.get("/ping")
    assert response.status_code == HTTPStatus.OK
    assert response.text == "pong"
