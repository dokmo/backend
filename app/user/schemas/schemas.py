from app.user.model.User import User

# 스키마에 대한 예시
class UserSchema:
    def __init__(self, idx: int, user_id: str, nickname: str):
        self.idx = idx
        self.user_id = user_id
        self.nickname = nickname

    @classmethod
    def from_orm(cls, user: User):
        return cls(
            idx=user.idx,
            user_id=user.user_id,
            nickname=user.nickname
        )