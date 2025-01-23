from app.user.domain.user import User
from app.user.infrastructure.repository.user_repository import UserRepository
import uuid

class UserService:
    def __init__(self):
        self.__meet_repository = UserRepository()

    async def find_user(self, user_id: uuid.UUID) -> User:
        return await self.__meet_repository.find_user(user_id= user_id)

    async def find_user_by_kakao_id(self, kakao_id: int) -> User:
        return await self.__meet_repository.find_user_by_kakao_id(kakao_id=kakao_id)

    async def sign_up(self, kakao_user_id:int, nickname:str):
        await self.__meet_repository.sign_up(kakao_user_id=kakao_user_id, nickname=nickname)
