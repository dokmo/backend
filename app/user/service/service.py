from app.user.model.User import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, kakao_user_id: str):
        async with self.session() as session:
            result = await session.execute(select(User).filter(User.kakao_user_id == kakao_user_id))
            user = result.scalars().first()  # 첫 번째 사용자만 반환
            return user

    async def create_user(self, user_id: str, nickname: str, kakao_user_id: str):
        async with self.session() as session:
            user = User(user_id=user_id, nickname=nickname, kakao_user_id=kakao_user_id)
            session.add(user)
            await session.commit()
            return user

    async def get_all_users(self):
        async with self.session() as session:
            result = await session.execute(select(User))
            users = result.scalars().all()
            return users

    async def update_user(self, user_id: str, nickname: str):
        async with self.session() as session:
            user = await session.execute(select(User).filter(User.user_id == user_id))
            user = user.scalars().first()
            if user:
                user.nickname = nickname
                await session.commit()
                return user
            return None
