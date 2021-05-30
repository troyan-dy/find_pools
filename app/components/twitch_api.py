from typing import Any, cast

from fastapi import Request
from fastapi_components.components.base import BaseComponent
from fastapi_components.logging import LoggerMixin
from fastapi_components.state import State


class TwitchApi(BaseComponent, LoggerMixin):
    async def startup(self, state: State) -> State:
        self.session = state.session
        state.twitch_api = self
        return state

    async def shutdown(self) -> None:
        pass

    async def ping(self) -> None:
        self.logger.info("PING")

    async def get_category(self, category: str) -> list[Any]:
        url = "https://api.twitch.tv/kraken/streams/?game=Pools, Hot Tubs, and Beaches"
        names = []
        limit = 100
        params = {"game": category, "limit": limit, "offset": 0}
        headers = {"Accept": "application/vnd.twitchtv.v5+json", "Client-ID": "i38s94bpzao27eszx5zgoqnqn9fq55"}
        while 1:
            r = await self._get(url, params=params, headers=headers, raise_for_status=True, verify_ssl=False)

            streams = r.get("streams", [])
            _names = [s["channel"]["name"] for s in streams]
            names += _names
            params["offset"] += limit  # type: ignore
            self.logger.info(f"len(_urls): {len(_names)}")
            if len(_names) != limit:
                break
        return names

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
