import uuid

from app.user.domain.user import User
from typing import List

class UserRepository:
    async def get_user_by_kakao_id(self, kakao_id: str) -> User:
        pass

    async def get_users(self, users: List[uuid.UUID]) -> list[User]:
        pass