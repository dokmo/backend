from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID


@dataclass
class UserData:
    user_id: UUID
    user_name: str

@dataclass
class MeetResponseData:
    meet_id: UUID
    meet_name: str
    description: Optional[str]
    participants: List[UserData]
    creator_id: UUID
    creator_name: str
