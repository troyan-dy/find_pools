import aiohttp
from starlette.datastructures import State

from app.components.base import BaseComponent


class AIOHTTPSessionComponent(BaseComponent):
    def __init__(self) -> None:
        self.session: aiohttp.ClientSession | None = None

    async def startup(self, state: State) -> State:
        self.session = aiohttp.ClientSession()
        state.session = self.session
        return state

    async def shutdown(self) -> None:
        if self.session is not None:
            await self.session.close()
