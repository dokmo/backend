import uuid


class Meet:

    def __init__(self, meet_name: str, creator_id: int, creator_name: str, description: str):
        self._meet_id = uuid.uuid4()
        self.meet_name: str = meet_name
        self.creator_id: int = creator_id
        self.creator_name: str = creator_name
        self.description: str = description
        self.participants: dict = dict()