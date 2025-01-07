from fastapi import APIRouter

example_router = APIRouter()

from core.fastapi.middlewares.auth import skip_jwt_verification



@example_router.get(path="")
async def hello_world():
    return "hello_world!"


@example_router.get(path="/protected")
async def hello_world():
    return "protected hello_world!"