import uuid

from app.user.infrastructure.model.user import UserModel
from sqlalchemy.future import select

from core.db.session import session_factory
from core.utils import Singleton


class UserRepository(metaclass=Singleton):

    async def find_user(self, user_id: uuid.UUID):
        query = (
            select(UserModel)
            .filter(UserModel.user_id == user_id)
        )

        async with session_factory() as session:
            result = await session.execute(query)
            user = result.scalars().one()
            return user

    async def sign_up(self, user_id:uuid.UUID, nickname:str):

        user = UserModel(
            user_id=user_id,
            nickname=nickname
        )
        async with session_factory() as session:
            session.add(user)
            await session.commit()
            return user

