from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID

from fastapi_pagination.bases import BasePage

from app.meet.domain.meet import Meet


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

def domain_to_response(meet:Meet) -> MeetResponseData:
    meet_response_data = MeetResponseData(
        meet_id=meet.meet_id,
        meet_name=meet.meet_name,
        description=meet.description,
        creator_id=meet.creator_id,
        creator_name=meet.creator_name,
        participants = meet.participants if meet.participants else []
    )

    return meet_response_data


class PaginatedResponse(BasePage[MeetResponseData]):
    items: List[MeetResponseData]
    total: int