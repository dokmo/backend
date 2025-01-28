from typing import List

from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from sqlalchemy.types import String
from uuid import UUID

from app.meet.domain.meet import Meet
from core.db import Base, TimeStamp


class Participants(Base, TimeStamp):
    __tablename__ = "meet_user_bindings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    meet_id: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)
    approval: Mapped[str] = mapped_column(String(4096), nullable=False)


class MeetModel(Base, TimeStamp):
    __tablename__ = "meet"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    meet_id: Mapped[UUID] = mapped_column(unique=True)
    meet_name: Mapped[str] = mapped_column(String(256), nullable=False)
    creator_id: Mapped[int] = mapped_column(nullable=False)
    creator_name: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str | None] = mapped_column(String(4096), nullable=True)

    @classmethod
    def from_domain(cls, *, meet: Meet):
        return cls(
            meet_id = meet.meet_id,
            meet_name = meet.meet_name,
            creator_id = meet.creator_id,
            creator_name = meet.creator_name,
            description = meet.description
        )

    def to_domain(self, creator_id:UUID, participants: List[Participants] = None) -> Meet:
        return Meet(
            meet_id=self.meet_id,
            meet_name=self.meet_name,
            creator_id=creator_id,
            creator_name=self.creator_name,
            description=self.description,
            participants=[
                participant.user_id for participant in (participants or [])
            ]
        )