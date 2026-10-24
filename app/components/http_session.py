from typing import Optional

import aiohttp
from starlette.datastructures import State

from app.components.base import BaseComponent


class AIOHTTPSessionComponent(BaseComponent):
    session: Optional[aiohttp.ClientSession] = None

    async def startup(self, state: State) -> State:
        self.session = aiohttp.ClientSession()
        state.session = self.session
        return state

    async def shutdown(self) -> None:
        if self.session:
            await self.session.close()
