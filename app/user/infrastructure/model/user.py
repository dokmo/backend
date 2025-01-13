from core.db import TimeStamp, Base

from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from sqlalchemy.types import String
from uuid import UUID

class UserModel(Base, TimeStamp):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    kakao_id: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[UUID] = mapped_column(unique=True)
    nickname: Mapped[str] = mapped_column(String, nullable=False)
