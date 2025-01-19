import uuid

from app.user.infrastructure.repository.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.__meet_repository = UserRepository()

    def find_user(self, kakao_user_id:int):
        self.__meet_repository.find_user(kakao_user_id= kakao_user_id)

    def sign_up(self, kakao_user_id:int, nickname:str):
        self.__meet_repository.sign_up(kakao_user_id=kakao_user_id, nickname=nickname)
