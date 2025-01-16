from dataclasses import dataclass

# FIXME Pydantic version issue with fastAPI
# from pydantic import BaseModel

@dataclass
class UserLoginInfo:
    access_token: str
    refresh_token: str
    user_id: int
    user_name: str
