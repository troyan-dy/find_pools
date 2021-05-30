import asyncio
from typing import Any, cast

from fastapi import Request
from fastapi_components.components.base import BaseComponent
from fastapi_components.logging import LoggerMixin
from fastapi_components.state import State


class TwitchApi(BaseComponent, LoggerMixin):
    async def startup(self, state: State) -> State:
        self.session = state.session
        self.client_id = state.settings.client_id
        state.twitch_api = self
        return state

    async def shutdown(self) -> None:
        pass

    async def ping(self) -> None:
        self.logger.info("PING")

    async def get_category(self, category: str) -> list[Any]:
        names = []
        coros = [self._get_names(category=category, limit=100, offset=i * 100) for i in range(4)]
        _names = await asyncio.gather(*coros)
        for _n in _names:
            names += _n
        return names

    async def _get_names(self, category, limit=100, offset=0):
        params = {"game": category, "limit": limit, "offset": offset}
        headers = {"Accept": "application/vnd.twitchtv.v5+json", "Client-ID": self.client_id}
        url = "https://api.twitch.tv/kraken/streams/"
        r = await self._get(url, params=params, headers=headers, raise_for_status=True, verify_ssl=False)

        streams = r.get("streams", [])
        _names = [s["channel"]["name"] for s in streams]
        self.logger.info(f"len(_names): {len(_names)}, limit: {limit}, offset: {offset}")
        return _names

    async def get_boobs_stream(self) -> list[Any]:
        return await self.get_category(category="Pools, Hot Tubs, and Beaches")

    async def get_chatting(self) -> list[Any]:
        return await self.get_category(category="Just Chatting")

    async def get_asmr(self) -> list[Any]:
        return await self.get_category(category="ASMR")

    async def _get(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        async with self.session.get(*args, **kwargs) as r:
            result = await r.json()
            return cast(dict[str, Any], result)


async def get_twitch_api(request: Request) -> TwitchApi:
    return cast(TwitchApi, request.app.state.twitch_api)
