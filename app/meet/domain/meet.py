import uuid
from typing import List


class Meet:

    def __init__(self, meet_name: str,creator_id: uuid.UUID,
                 creator_name: str, description: str, meet_id: uuid.UUID = uuid.uuid4(),
                 participants = None):
        if participants is None:
            participants = []
        self.meet_id: uuid.UUID = uuid.uuid4()
        self.meet_name: str = meet_name
        self.creator_id: uuid.UUID = creator_id
        self.creator_name: str = creator_name
        self.description: str = description
        self.participants: List[int] = participants
