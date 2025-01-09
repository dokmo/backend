from dataclasses import dataclass

from pydantic import BaseModel

@dataclass
class UserLoginInfo(BaseModel):
    access_token: str
    refresh_token: str
    user_id: int
    user_name: str
