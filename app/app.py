import uvicorn
from fastapi import APIRouter, FastAPI
from starlette.responses import PlainTextResponse

api_router = APIRouter()


@api_router.get("/ping")
async def ping() -> PlainTextResponse:
    return PlainTextResponse("pong")


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)
    return app


app = create_app()
if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)
