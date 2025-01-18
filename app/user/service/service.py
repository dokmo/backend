import uuid

from app.user.infrastructure.repository.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.__meet_repository = UserRepository()


    def sign_up(self, user_id:uuid.UUID, nickname:str):
        self.__meet_repository.sign_up(user_id=user_id, nickname=nickname)

    def find_user(self, user_id):
        self.__meet_repository.find_user(user_id = user_id)