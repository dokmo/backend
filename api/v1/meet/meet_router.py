import uuid

from fastapi import APIRouter, Depends
from fastapi_pagination import Params

from api.v1.Response import DefaultResponse
from app.meet.application.dto.meet_request import MeetCreateRequest, MeetJoinRequest
from app.meet.application.dto.meet_response import MeetResponseData, domain_to_response
from app.meet.application.service.meet import MeetService
from app.meet.domain.meet import Meet
from core.fastapi.jwt_verifier import try_validate_token, require_authorization

meet_router = APIRouter()
meet_service = MeetService()


@meet_router.get(path="")
async def get_meets(
        user_id: uuid.UUID = Depends(try_validate_token), pagination: Params = Depends()
) -> DefaultResponse:
    if user_id is None:
        meets = await meet_service.get_meets(pagination=pagination)
    else:
        meets = await meet_service.get_my_meets(pagination=pagination, user_id=user_id)

    response: DefaultResponse = DefaultResponse.create_response(data=meets)

    return response


@meet_router.get(path="/detail")
async def get_meet_detail(
        meet_id: uuid.UUID,
        user_id: uuid.UUID = Depends(require_authorization)
) -> DefaultResponse[MeetResponseData]:

    meet_detail: Meet = await meet_service.get_meet_detail(meet_id=meet_id)
    if meet_detail.creator_id == user_id:
        meet_detail: Meet = await meet_service.get_my_meet_detail(meet_id=meet_id, user_id=user_id)

    data: MeetResponseData = domain_to_response(meet_detail)
    response: DefaultResponse[MeetResponseData] = DefaultResponse.create_response(data=data)
    return response


@meet_router.post(path="")
async def create_meet(
        request_dto: MeetCreateRequest,
        user_id: uuid.UUID = Depends(require_authorization)
):
    await meet_service.create_meet(request = request_dto, creator_id= user_id)


@meet_router.post(path="/join")
async def join_meet(
        request_dto: MeetJoinRequest,
        user_id: uuid.UUID = Depends(require_authorization)
):
    await meet_service.join_meet(request = request_dto)


@meet_router.patch(path="/join")
async def approve_or_decline_join(
        request_dto: MeetJoinRequest,
        user_id: uuid.UUID = Depends(require_authorization)
):
    await meet_service.approve_or_decline_join(request = request_dto)
