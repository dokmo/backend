from dataclasses import dataclass

# from pydantic import BaseModel

@dataclass
class TokenResponseData:
    access_token: str
    user_name: str