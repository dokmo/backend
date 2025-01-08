from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from starlette.requests import Request

from api.v1.Response import DefaultResponse
from app.meet.application.dto.meet_request import MeetCreateRequest
from app.meet.application.dto.meet_response import MeetResponseData

meet_router = APIRouter()

@meet_router.get(path="")
async def get_meets(pagination: Params = Depends()) -> DefaultResponse[Page[MeetResponseData]]:
    pass


@meet_router.post(path="")
async def create_meet(request_dto: MeetCreateRequest):
    user_id: int = 0 # FIXME

