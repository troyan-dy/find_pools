import uvicorn
from fastapi import APIRouter, Depends, FastAPI
from fastapi_components.components.http_session import AIOHTTPSessionComponent
from fastapi_components.logging import LoggerSettings, setup_logging
from fastapi_components.state_manager import FastAPIStateManager
from pydantic import BaseSettings
from pydantic.types import PositiveInt
from starlette.responses import PlainTextResponse

from app.components.twitch_api import TwitchApi, get_twitch_api

api_router = APIRouter()


class Settings(BaseSettings):
    log: LoggerSettings = LoggerSettings()
    client_id: str
    port: PositiveInt = 8000

    class Config:
        env_file = "local.env"


@api_router.get("/ping")
async def ping(ta: TwitchApi = Depends(get_twitch_api)) -> PlainTextResponse:
    await ta.ping()
    return PlainTextResponse("pong")


# get_boobs_stream


@api_router.get("/get_boobs_stream")
async def get_boobs_stream(ta: TwitchApi = Depends(get_twitch_api)) -> PlainTextResponse:
    result = await ta.get_boobs_stream()
    return PlainTextResponse(str(result))


@api_router.get("/get_chatting")
async def get_chatting(ta: TwitchApi = Depends(get_twitch_api)) -> PlainTextResponse:
    result = await ta.get_chatting()
    return PlainTextResponse(str(result))


@api_router.get("/get_asmr")
async def get_asmr(ta: TwitchApi = Depends(get_twitch_api)) -> PlainTextResponse:
    result = await ta.get_asmr()
    return PlainTextResponse(str(result))


def create_app(settings: Settings) -> FastAPI:
    setup_logging(settings.log)
    state_manager = FastAPIStateManager(
        components=[AIOHTTPSessionComponent(), TwitchApi()],
        settings=settings,
    )

    app = FastAPI()
    app.include_router(api_router)

    state_manager.set_startup_hook(app)
    state_manager.set_shutdown_hook(app)

    return app


settings = Settings()
app = create_app(settings=settings)
if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=settings.port)
