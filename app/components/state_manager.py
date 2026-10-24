from collections.abc import AsyncIterator
from contextlib import AsyncExitStack, asynccontextmanager

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
        async with AsyncExitStack() as shutdown_stack:
            for component in self.components:
                # Startup is sequential by design: each component reads what the previous ones put into state.
                state = await component.startup(state)  # noqa: WPS476
                shutdown_stack.push_async_callback(component.shutdown)

            yield
