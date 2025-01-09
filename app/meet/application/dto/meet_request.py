from dataclasses import dataclass
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


@dataclass
class MeetCreateRequest(BaseModel):
    meet_name: str
    description: Optional[str] = None


class Operations(str, Enum):
    ACCEPT = "ACCEPT"
    DECLINE = "DECLINE"

@dataclass
class MeetJoinRequest(BaseModel):
    meet_id: UUID
    operation: Operations
    target_user_id: UUID