from wsgiref import headers

from fastapi import APIRouter, Request


example_router = APIRouter()

@example_router.get(path="")
async def hello_world():
    return "hello_world!"


@example_router.get(path="/protected") #FIXME(jwt 미들웨어 테스트용 url입니다.)
async def hello_world():
    return {"message":"protected hello_world!"}