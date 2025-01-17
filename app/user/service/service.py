from app.user.infrastructure.repository.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.__meet_repository = UserRepository()
