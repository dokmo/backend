from sqlalchemy import String
from uuid import uuid4

from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from core.db import Base, TimeStamp


class User(Base, TimeStamp):
# class User():
    __tablename__ = 'USER'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    kakao_id: Mapped[int] = mapped_column(unique=True)
    user_id: Mapped[int] = mapped_column(default=str(uuid4()))
    nickname: Mapped[str] = mapped_column(String)
