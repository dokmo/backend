from dataclasses import dataclass

@dataclass
class UserCreateRequest():
    user_nickname: str

@dataclass
class UserUpdateRequest():
    user_nickname: str


