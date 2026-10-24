import asyncio
import itertools
from typing import Annotated, Any, Final, cast

import aiohttp
from fastapi import Depends, Request
from starlette.datastructures import State

from app.components.base import BaseComponent
from app.components.logging import LoggerMixin

KRAKEN_STREAMS_URL: Final = "https://api.twitch.tv/kraken/streams/"
KRAKEN_ACCEPT_HEADER: Final = "application/vnd.twitchtv.v5+json"
STREAMS_PAGE_SIZE: Final = 100
STREAMS_PAGES_COUNT: Final = 4


class KrakenStreamsClient(LoggerMixin):
    """Client for the ``/kraken/streams/`` endpoint of the Twitch API v5."""

    def __init__(self, session: aiohttp.ClientSession, client_id: str) -> None:
        self.session = session
        self.headers = {"Accept": KRAKEN_ACCEPT_HEADER, "Client-ID": client_id}

    async def get_channel_names(self, category: str, limit: int = STREAMS_PAGE_SIZE, offset: int = 0) -> list[str]:
        query_params = {"game": category, "limit": limit, "offset": offset}
        response_json = await self._get_json(query_params)

        streams = response_json.get("streams", [])
        channel_names = [stream["channel"]["name"] for stream in streams]
        self.logger.info(f"len(_names): {len(channel_names)}, limit: {limit}, offset: {offset}")
        return channel_names

    async def _get_json(self, query_params: dict[str, Any]) -> dict[str, Any]:
        async with self.session.get(
            KRAKEN_STREAMS_URL,
            params=query_params,
            headers=self.headers,
            raise_for_status=True,
            ssl=False,
        ) as response:
            response_json = await response.json()
        return cast(dict[str, Any], response_json)


class TwitchApi(BaseComponent, LoggerMixin):
    async def startup(self, state: State) -> State:
        self.streams_client = KrakenStreamsClient(session=state.session, client_id=state.settings.client_id)
        state.twitch_api = self
        return state

    async def shutdown(self) -> None:
        """Nothing to release: the HTTP session belongs to ``AIOHTTPSessionComponent``."""

    async def ping(self) -> None:
        self.logger.info("PING")

    async def get_category(self, category: str) -> list[str]:
        pages = await asyncio.gather(
            *(
                self.streams_client.get_channel_names(
                    category=category,
                    limit=STREAMS_PAGE_SIZE,
                    offset=page_index * STREAMS_PAGE_SIZE,
                )
                for page_index in range(STREAMS_PAGES_COUNT)
            ),
        )
        return list(itertools.chain.from_iterable(pages))

    async def get_boobs_stream(self) -> list[str]:
        return await self.get_category(category="Pools, Hot Tubs, and Beaches")

    async def get_chatting(self) -> list[str]:
        return await self.get_category(category="Just Chatting")

    async def get_asmr(self) -> list[str]:
        return await self.get_category(category="ASMR")


async def get_twitch_api(request: Request) -> TwitchApi:
    return cast(TwitchApi, request.app.state.twitch_api)


TwitchApiDependency = Annotated[TwitchApi, Depends(get_twitch_api)]
