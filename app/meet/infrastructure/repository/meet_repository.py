import uuid
from typing import List

from sqlalchemy import select

from app.meet.domain.meet import Meet
from app.meet.infrastructure.model.meet import MeetModel, Participants
from core.db.session import session_factory
from core.utils import Singleton

class MeetRepository(metaclass=Singleton):

    async def get_meets(self) -> List[Meet]:
        query = select(MeetModel)
        async with session_factory() as read_session:
            result = await read_session.execute(query)
        meets: List[MeetModel] = result.scalars().all()
        return [ meet.to_domain() for meet in meets ]

    async def get_user_meets(self, user_id:uuid.UUID) -> List[Meet]:
        query = select(Participants).where(Participants.user_id == user_id).order_by(Participants.created_at.desc())
        async with session_factory() as read_session:
            result = await read_session.execute(query)
            meet_id_list = [participant.meet_id for participant in result.scalars()]

            meet_query = select(MeetModel).where(MeetModel.meet_id.in_(meet_id_list))
            meets_result = await read_session.execute(meet_query)

        meet_models = meets_result.scalars().all()

        return [meet_model.to_domain(participants=[]) for meet_model in meet_models]

    async def get_meet_detail(self, meet_id) -> Meet:
        query = select(MeetModel).where(MeetModel.meet_id == meet_id).order_by(MeetModel.created_at.desc())
        participants_query = select(Participants).where(Participants.meet_id == meet_id)
        async with session_factory() as read_session:
            result = await read_session.execute(query)
            participants_result = await read_session.execute(participants_query)

        meet_model = result.scalars().all()
        participants_model = participants_result.scalars().all()
        meet = meet_model.to_domain()
        participants = participants_model.to_domain()

        return meet.to_domain(participants=participants)
