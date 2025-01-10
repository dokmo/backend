import uuid
from typing import List

from app.meet.domain.meet import Meet
from app.meet.infrastructure.repository import MeetRepository
from core.utils import Singleton

class MeetService(metaclass=Singleton):
    def __init__(self):
        self.__repository = MeetRepository()

    async def get_meets(self) -> List[Meet]:
        meets: List[Meet] = await self.__repository.get_meets()
        return meets

    async def get_my_meets(self, user_id: uuid.UUID) -> List[Meet]:
        meets: List[Meet] = await self.__repository.get_user_meets(user_id=user_id)
        return meets

    async def get_meet_detail(self, meet_id) -> Meet:
        meet: Meet = await self.__repository.get_meet_detail(meet_id=meet_id)
        return meet

    async def get_my_meet_detail(self, meet_id, user_id):
        meet: Meet = await self.__repository.get_my_meet_detail(meet_id=meet_id, user_id=user_id)
        pass


