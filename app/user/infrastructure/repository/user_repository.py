import uuid

from app.user.infrastructure.model.user import UserModel
from sqlalchemy.future import select

from core.db.session import session_factory
from core.utils import Singleton


class UserRepository(metaclass=Singleton):

    async def find_user(self, kakao_user_id: int):
        query = (
            select(UserModel)
            .filter(UserModel.kakao_id == kakao_user_id)
        )

        async with session_factory() as session:
            result = await session.execute(query)
            user = result.scalars().first()
            return user

    async def sign_up(self, kakao_user_id:int, nickname:str):

        user = UserModel(
            kakao_id=kakao_user_id,
            nickname=nickname
        )
        async with session_factory() as session:
            session.add(user)
            await session.commit()
            return user

