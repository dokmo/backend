from typing import List

from fastapi import FastAPI, Depends
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from api.root_router import root_router
from core.exception.error_base import CustomException
from core.exception.exception_handlers import custom_exception_handler
from core.fastapi.logging import Logging
from core.fastapi.middlewares import ResponseLogMiddleware
from core.fastapi.middlewares.auth import VerifyTokenMiddleware
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
        Middleware(ResponseLogMiddleware),
        # Middleware(VerifyTokenMiddleware)
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
        middleware=init_middleware()
    )
    init_routers(_app=_app)
    init_exception_handlers(_app=_app)
    return _app

app = init_app()