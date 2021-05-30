from fastapi import Request
from fastapi_components.components.base import BaseComponent
from fastapi_components.logging import LoggerMixin
from fastapi_components.state import State


class TwitchApi(BaseComponent, LoggerMixin):
    async def startup(self, state: State) -> State:
        self.session = state.session
        state.twitch_api = self
        return state

    async def shutdown(self):
        pass

    async def ping(self):
        self.logger.info("PING")

    async def get_category(self, category):
        url = "https://api.twitch.tv/kraken/streams/?game=Pools, Hot Tubs, and Beaches"
        urls = []
        limit = 100
        params = {"game": category, "limit": limit, "offset": 0}
        headers = {"Accept": "application/vnd.twitchtv.v5+json", "Client-ID": "i38s94bpzao27eszx5zgoqnqn9fq55"}
        while 1:
            r = await self._get(url, params=params, headers=headers, raise_for_status=True, verify_ssl=False)

            streams = r.get("streams", [])
            _urls = [s["channel"]["url"] for s in streams]
            urls += _urls
            params["offset"] += limit
            self.logger.info(f"len(_urls): {len(_urls)}")
            if len(_urls) != limit:
                break
        return urls

    async def get_boobs_stream(self):
        return await self.get_category(category="Pools, Hot Tubs, and Beaches")

    async def get_chatting(self):
        return await self.get_category(category="Just Chatting")

    async def get_asmr(self):
        return await self.get_category(category="ASMR")

    async def _get(self, *args, **kwargs):
        async with self.session.get(*args, **kwargs) as r:
            return await r.json()


async def get_twitch_api(request: Request) -> TwitchApi:
    return request.app.state.twitch_api
