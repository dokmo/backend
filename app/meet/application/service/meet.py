from typing import List

from fastapi_pagination import Params, Page
from fastapi_pagination.async_paginator import paginate

from app.meet.domain.meet import Meet
from app.meet.infrastructure.repository import MeetRepository
from core.utils import Singleton


class MeetService(metaclass=Singleton):
    def __init__(self):
        self.__repository = MeetRepository()

    async def get_meets(self, pagination: Params = None) -> Page[Meet]:
        meets: List[Meet] = await self.__repository.get_meets()
        return await paginate(meets, pagination)




meet_service = MeetService()