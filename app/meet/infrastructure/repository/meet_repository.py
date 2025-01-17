import uuid
from typing import List

from fastapi_pagination import Params
from sqlalchemy import select

from app.meet.application.dto.meet_request import MeetJoinRequest, MeetCreateRequest, Operations
from app.user.infrastructure.model.user import UserModel
from app.meet.domain.meet import Meet
from app.meet.infrastructure.model.meet import MeetModel, Participants
from core.db.session import session_factory
from core.utils import Singleton
from fastapi_pagination import paginate

class MeetRepository(metaclass=Singleton):

    async def get_meets(self, pagination: Params):

        page = pagination.page
        size = pagination.size
        skip = (page - 1) * size

        query = (
            select(MeetModel, UserModel)
            .join(UserModel, UserModel.id == MeetModel.creator_id)
            .order_by(MeetModel.created_at.desc())
            .offset(skip)
            .limit(size)
        )

        async with session_factory() as read_session:
            result = await read_session.execute(query)

        meets_and_users = result.scalars().all()

        # meets: List[Meet] = []
        # if len(meets_and_users) != 0:
        #     for meet_model, user in meets_and_users:
        #         meet = meet_model.to_domain(creator_id = user.user_id)
        #         meets.append(meet)
        data = paginate(meets_and_users, pagination)
        return data

    async def get_my_meets(self, pagination, user_id:uuid.UUID) -> List[Meet]:
        query = (
            select(MeetModel, UserModel, Participants)
            .join(Participants, MeetModel.id == Participants.meet_id)
            .join(UserModel, Participants.user_id == UserModel.id)
            .where(UserModel.user_id == user_id)
            .order_by(MeetModel.created_at.desc())
        )

        async with session_factory() as read_session:
            result = await read_session.execute(query)

        meet_models_and_users_and_participants = result.all()

        meets: List[Meet] = []
        if len(meet_models_and_users_and_participants) != 0:
            for meet_model, user, participants in meet_models_and_users_and_participants:
                meet = meet_model.to_domain(creator_id = user.user_id)
                meets.append(meet)
        return meets

    async def get_meet_detail(self, meet_id:uuid.UUID) -> Meet:

        query = (
            select(MeetModel, UserModel)
            .join(UserModel, UserModel.id == MeetModel.creator_id)
            .where(MeetModel.meet_id == meet_id)
            .order_by(MeetModel.created_at.desc())
        )

        async with session_factory() as read_session:
            result = await read_session.execute(query)
        meet_model, user = result.all()
        meet: Meet = meet_model.to_domain(creator_id=user.user_id)

        return meet

    async def get_my_meet_detail(self, meet_id:uuid.UUID, user_id:uuid.UUID) -> Meet:

        query = (select(MeetModel, UserModel, Participants)
                 .join(UserModel, UserModel.user_id == user_id)
                 .where(MeetModel.creator_id == UserModel.id)
                 .where(MeetModel.meet_id == meet_id)
                 .order_by(MeetModel.created_at.desc()))

        async with session_factory() as read_session:
            result = await read_session.execute(query)

        meet_model, user, participants = result.scalars().one()
        meet = meet_model.to_domain(participants=participants)

        return meet

    async def create_meet(self, request: MeetCreateRequest, create_id:uuid.UUID):
        query = select(UserModel).where(UserModel.user_id == create_id)

        async with session_factory() as read_session:
            result = await read_session.execute(query)
            user = result.scalars().one()

        if user is None:
            raise Exception("User not found")


        meet_model = MeetModel(
            meet_id=uuid.uuid4(),
            meet_name=request.meet_name,
            creator_id=user.id,
            creator_name=user.nickname,
            description=request.description
        )

        async with session_factory() as write_session:
            write_session.add(meet_model)
            await write_session.commit()

    async def join_meet(self, request: MeetJoinRequest):
        user_query = select(UserModel).where(UserModel.user_id == request.target_user_id)
        meet_query = select(MeetModel).where(MeetModel.meet_id == request.meet_id)


        async with session_factory() as read_session:
            user_result = await read_session.execute(user_query)
            meet_result = await read_session.execute(meet_query)

            user = user_result.scalars().one()
            meet = meet_result.scalars().one()

            check_query = (
                select(Participants)
                .where(Participants.meet_id == meet.id)
                .where(Participants.user_id == user.id)
            )

            check_result = await read_session.execute(check_query)

        if check_result.scalars().one() is None:
            participants: Participants = Participants(
                meet_id=meet.id,
                user_id=user.id,
                approval=Operations.DECLINE
            )
            async with session_factory() as write_session:
                write_session.add(participants)
                await write_session.commit()


    async def approve_or_decline_join(self, request: MeetJoinRequest):
        query = (
            select(MeetModel, UserModel)
            .join(UserModel, UserModel.id == MeetModel.creator_id)
            .where(UserModel.user_id == request.creator_id)
            .where(MeetModel.meet_id == request.meet_id)
        )
        async with session_factory() as read_session:
            result = await read_session.execute(query)

            meet_model, user_model = result.scalars().one()
            if meet_model is None:
                return #FIXME
            elif user_model is None:
                return

            query = (
                select(Participants)
                .where(Participants.meet_id == meet_model.id)
                .where(Participants.user_id == user_model.id)
            )

            result = await read_session.execute(query)
            result = result.scalars().one()
            result.approval = request.operation

        async with session_factory() as write_session:
            write_session.add(result)
            await write_session.commit()