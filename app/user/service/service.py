from app.user.infrastructure.model.user import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class UserService:
    def __init__(self, session: AsyncSession):
        self.__meet_repository = session #FIXME
    async def get_user(self, kakao_user_id: str):
        async with self.__meet_repository() as session:
            result = await session.execute(select(UserModel).filter(UserModel.kakao_user_id == kakao_user_id))
            user = result.scalars().first()  # 첫 번째 사용자만 반환
            return user

    async def create_user(self, user_id: str, nickname: str, kakao_user_id: str):
        async with self.__meet_repository() as session:
            user = UserModel(user_id=user_id, nickname=nickname, kakao_user_id=kakao_user_id)
            session.add(user)
            await session.commit()
            return user

    async def get_all_users(self):
        async with self.__meet_repository() as session:
            result = await session.execute(select(UserModel))
            users = result.scalars().all()
            return users

    async def update_user(self, user_id: str, nickname: str):
        async with self.__meet_repository() as session:
            user = await session.execute(select(UserModel).filter(UserModel.user_id == user_id))
            user = user.scalars().first()
            if user:
                user.nickname = nickname
                await session.commit()
                return user
            return None
