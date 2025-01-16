from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, Depends
from fastapi_pagination import add_pagination
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from api.root_router import root_router
from core.db.session import engines, EngineType, Base
from core.exception.error_base import CustomException
from core.exception.exception_handlers import custom_exception_handler
from core.fastapi.logging import Logging
from core.fastapi.middlewares import ResponseLogMiddleware
from core.fastapi.middlewares.sqlalchemy import SQLAlchemyMiddleware

def init_routers(_app: FastAPI) -> None:
    _app.include_router(router=root_router)


def init_exception_handlers(_app: FastAPI) -> None:
    _app.add_exception_handler(CustomException, custom_exception_handler)


def init_middleware() -> List[Middleware]:
    middlewares = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(SQLAlchemyMiddleware),
        Middleware(ResponseLogMiddleware)
    ]
    return middlewares


def init_app() -> FastAPI:
    _app = FastAPI(
        title="Python MicroService App",
        description="Microservice templates",
        version="0.0.1",
        docs_url="/swagger_ui",
        redoc_url="/redoc",
        dependencies=[Depends(Logging)],
        middleware=init_middleware(),
        lifespan=lifespan
    )
    init_routers(_app=_app)
    init_exception_handlers(_app=_app)
    #pagination lib
    add_pagination(_app)
    return _app

@asynccontextmanager
async def lifespan(_app: FastAPI):
    await initialize_database_tables()
    yield


async def initialize_database_tables():
    engine: AsyncEngine = engines[EngineType.WRITER]
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)



app = init_app()
