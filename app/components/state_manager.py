from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from pydantic_settings import BaseSettings

from app.components.base import BaseComponent


class FastAPIStateManager:
    """Манагер стейта для FastAPI."""

    def __init__(self, components: list[BaseComponent], settings: BaseSettings) -> None:
        self.settings = settings
        self.components = components

    @asynccontextmanager
    async def lifespan(self, app: FastAPI) -> AsyncIterator[None]:
        """Последовательно вызовет startup каждого компонента, передавая в него app.state
        (изначально в нём только settings), а на остановке - shutdown в обратном порядке.
        """
        state = app.state
        state.settings = self.settings
        for component in self.components:
            state = await component.startup(state)

        yield

        for component in reversed(self.components):
            await component.shutdown()
