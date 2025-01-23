import uuid

from app.user.domain.user import User
from app.user.infrastructure.model.user import UserModel
from sqlalchemy.future import select

from core.db.session import session_factory
from core.utils import Singleton



class UserRepository(metaclass=Singleton):

    async def find_user(self, user_id: uuid) -> User:
        query = (
            select(UserModel)
            .filter(UserModel.user_id == user_id)
        )

        async with session_factory() as session:
            result = await session.execute(query)
            user_model: UserModel = result.scalars().first()

        return user_model.to_domain() if (user_model is not None) else None

    async def find_user_by_kakao_id(self, kakao_id: int) -> User:
        query = (
            select(UserModel)
            .filter(UserModel.kakao_id == kakao_id)
        )

        async with session_factory() as session:
            result = await session.execute(query)
            user_model: UserModel = result.scalars().first()

        return user_model.to_domain() if (user_model is not None) else None

    async def sign_up(self, kakao_user_id:int, nickname:str):

        user = UserModel(
            kakao_id=kakao_user_id,
            user_id=uuid.UUID(int=kakao_user_id),
            nickname=nickname
        )
        async with session_factory() as session:
            session.add(user)
            await session.commit()

        return user

