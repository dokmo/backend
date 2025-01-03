from fastapi import APIRouter

example_router = APIRouter()

@example_router.get(path="")
async def hello_world():
    return "hello_world!"

@example_router.post(path="")
async def hello_post(data: dict):
    return data