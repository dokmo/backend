from fastapi import APIRouter, Request


example_router = APIRouter()

@example_router.get(path="")
async def hello_world():
    return "hello_world!"


@example_router.get(path="/protected")
async def hello_world():
    return {"message":"protected hello_world!"}