from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from sqlalchemy.types import String, UUID

from app.meet.domain.meet import Meet
from core.db import Base, TimeStamp


class MeetModel(Base, TimeStamp):
    __tablename__ = "meet"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    meet_id: Mapped[UUID] = mapped_column(unique=True)
    meet_name: Mapped[str] = mapped_column(String, nullable=False)
    creator_id: Mapped[UUID] = mapped_column(nullable=False)
    creator_name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


    @classmethod
    def from_domain(cls, *, meet: Meet):
        return cls(
            meet_id = meet.meet_id
        )


class Participants(Base, TimeStamp):
    __tablename__ = "meet_user_bindings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    meet_id: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)