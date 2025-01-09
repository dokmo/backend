from dataclasses import dataclass

from pydantic import BaseModel

@dataclass
class TokenResponseData(BaseModel):
    access_token: str
    user_name: str