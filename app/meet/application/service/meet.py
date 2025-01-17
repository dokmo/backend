import uuid
from typing import List

from fastapi_pagination import Params

from app.meet.application.dto.meet_request import MeetJoinRequest, MeetCreateRequest
from app.meet.domain.meet import Meet
from app.meet.infrastructure.repository import MeetRepository
from app.user.infrastructure.repository.user_repository import UserRepository
from core.utils import Singleton

class MeetService(metaclass=Singleton):
    def __init__(self):
        self.__meet_repository = MeetRepository()

    async def get_meets(self, pagination: Params) -> List[Meet]:
        meets: List[Meet] = await self.__meet_repository.get_meets(pagination=pagination)
        return meets

    async def get_my_meets(self, pagination: Params, user_id: uuid.UUID) -> List[Meet]:
        meets: List[Meet] = await self.__meet_repository.get_my_meets(pagination=pagination, user_id=user_id)
        return meets

    async def get_meet_detail(self, meet_id: uuid.UUID) -> Meet:
        meet: Meet = await self.__meet_repository.get_meet_detail(meet_id=meet_id)
        return meet

    async def get_my_meet_detail(self, meet_id, user_id) -> Meet:
        meet: Meet = await self.__meet_repository.get_my_meet_detail(meet_id=meet_id, user_id=user_id)
        return meet

    async def create_meet(self, request: MeetCreateRequest, creator_id:uuid.UUID):
        await self.__meet_repository.create_meet(request=request, create_id=creator_id)

    async def join_meet(self, request: MeetJoinRequest):
        await self.__meet_repository.join_meet(request=request)

    async def approve_or_decline_join(self, request: MeetJoinRequest):
        await self.__meet_repository.approve_or_decline_join(request=request)



