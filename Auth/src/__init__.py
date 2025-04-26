from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.core.db import db_helper
from src.core.models.base import Base
from src.api.views import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_helper.init_database()
    yield


def create_app():
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)

    return app
