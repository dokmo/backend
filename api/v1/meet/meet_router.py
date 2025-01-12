import uuid

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params

from api.v1.Response import DefaultResponse
from app.meet.application.dto.meet_request import MeetCreateRequest, MeetJoinRequest
from app.meet.application.dto.meet_response import MeetResponseData, domain_to_response
from app.meet.application.service.meet import MeetService
from fastapi_pagination.async_paginator import paginate
from typing import List
from app.meet.domain.meet import Meet

meet_router = APIRouter()
meet_service = MeetService()

temporary_user_id = uuid.uuid4() #FIXME("토큰으로부터 받은 유저 정보")

@meet_router.get(path="")
async def get_meets(pagination: Params = Depends()) -> DefaultResponse[Page[MeetResponseData]]:

    meets: List[Meet] = await meet_service.get_meets()
    if len(meets) != 0:
        meets_response_data: List[MeetResponseData] = [domain_to_response(meet) for meet in meets]
        response: DefaultResponse[Page[MeetResponseData]] = DefaultResponse.create_response(data= await paginate(meets_response_data, pagination))
    else:
        data = await paginate([], pagination)
        response: DefaultResponse[Page[MeetResponseData]] = DefaultResponse.create_response(data=data)
    return response


@meet_router.get(path="/my_meets")
async def get_my_meets(
        pagination: Params = Depends(),
) -> DefaultResponse[Page[MeetResponseData]]:

    meets: List[Meet] = await meet_service.get_my_meets(user_id = temporary_user_id)
    meets_response_data: List[MeetResponseData] = [domain_to_response(meet) for meet in meets]
    response: DefaultResponse[Page[MeetResponseData]] = DefaultResponse.create_response(data= await paginate(meets_response_data, pagination))
    return response


@meet_router.get(path="/detail")
async def get_meet_detail(
        meet_id:uuid.UUID
) -> DefaultResponse[MeetResponseData]:
    meet_detail: Meet = await meet_service.get_meet_detail(meet_id = meet_id)
    detail_response_data:MeetResponseData = domain_to_response(meet_detail)
    response:DefaultResponse[MeetResponseData] = DefaultResponse.create_response(data=detail_response_data)
    return response


@meet_router.get(path="/my_detail")
async def get_my_meet_detail(
        meet_id:uuid.UUID
) -> DefaultResponse[MeetResponseData]:
    meet_detail: Meet = await meet_service.get_my_meet_detail(meet_id = meet_id, user_id = temporary_user_id)
    detail_response_data:MeetResponseData = domain_to_response(meet_detail)
    response:DefaultResponse[MeetResponseData] = DefaultResponse.create_response(data=detail_response_data)
    return response


@meet_router.post(path="/")
async def create_meet(request_dto: MeetCreateRequest):
    await meet_service.create_meet(request = request_dto, creator_id= temporary_user_id)


@meet_router.post(path="/join")
async def join_meet(request_dto: MeetCreateRequest):
    await meet_service.join_meet(request = request_dto)


@meet_router.patch(path="/join")
async def approve_or_decline_join(request_dto: MeetJoinRequest):
    await meet_service.approve_or_decline_join(request = request_dto)
