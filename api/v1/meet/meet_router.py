from fastapi import APIRouter
from starlette.requests import Request

meet_router = APIRouter()

@meet_router.get(path="")
async def get_meet(request: Request):
    pass