import random

import uvicorn
from fastapi import APIRouter, FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic.types import PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.responses import PlainTextResponse, Response

from app.components.http_session import AIOHTTPSessionComponent
from app.components.logging import LoggerSettings, setup_logging
from app.components.state_manager import FastAPIStateManager
from app.components.twitch_api import TwitchApi, TwitchApiDependency

api_router = APIRouter()
templates = Jinja2Templates(directory="templates")


class Settings(BaseSettings):
    log: LoggerSettings = LoggerSettings()
    client_id: str
    port: PositiveInt = 8000

    model_config = SettingsConfigDict(env_file="local.env")


def render_random_channel(request: Request, channel_names: list[str]) -> Response:
    channel_name = random.choice(channel_names)
    return templates.TemplateResponse(request, "index.html", {"channel_name": channel_name})


@api_router.get("/ping")
async def ping(twitch_api: TwitchApiDependency) -> PlainTextResponse:
    await twitch_api.ping()
    return PlainTextResponse("pong")


@api_router.get("/")
async def index(request: Request, twitch_api: TwitchApiDependency) -> Response:
    return render_random_channel(request, await twitch_api.get_boobs_stream())


@api_router.get("/asmr")
async def get_asmr(request: Request, twitch_api: TwitchApiDependency) -> Response:
    return render_random_channel(request, await twitch_api.get_asmr())


@api_router.get("/chatting")
async def get_chatting(request: Request, twitch_api: TwitchApiDependency) -> Response:
    return render_random_channel(request, await twitch_api.get_chatting())


def create_app(settings: Settings) -> FastAPI:
    setup_logging(settings.log)
    state_manager = FastAPIStateManager(
        components=[AIOHTTPSessionComponent(), TwitchApi()],
        settings=settings,
    )

    app = FastAPI(lifespan=state_manager.lifespan)
    app.include_router(api_router)

    return app


settings = Settings()
app = create_app(settings=settings)
if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=settings.port)
