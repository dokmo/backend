from typing import List

from sqlalchemy import select

from app.meet.domain.meet import Meet
from app.meet.infrastructure.model.meet import MeetModel
from core.db.session import session_factory
from core.utils import Singleton

class MeetRepository(metaclass=Singleton):

    async def get_meets(self) -> List[Meet]:
        query = select(MeetModel)
        async with session_factory() as read_session:
            result = await read_session.execute(query)
        meets: List[MeetModel] = result.scalars().all()
        return [ meet.to_domain() for meet in meets ]
