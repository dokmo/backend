from dataclasses import dataclass

from pydantic import BaseModel, ValidationError


@dataclass
class KakaoUserData(BaseModel):
    id: int
    nickname: str

class KakaoAccessTokenResponse(BaseModel):
    token_type: str
    access_token: str
    id_token: Optional[str] = None
    expires_in: int
    refresh_token: str
    refresh_token_expires_in: int
    scope: Optional[str] = None

class KakaoProperties(BaseModel):
    nickname: Optional[str] = None
    profile_image: Optional[str] = None
    thumbnail_image: Optional[str] = None

class KakaoUserResponse(BaseModel):
    id: int
    properties: Optional[KakaoProperties] = None


def mapping_access_token(response_json: dict) -> KakaoAccessTokenResponse:
    try:
        return KakaoAccessTokenResponse(**response_json)
    except ValidationError as e:
        raise ValueError(f"Invalid response format: {e}")

def mapping_user_data(response_json: dict) -> KakaoUserResponse:
    try:
        return KakaoUserResponse(**response_json)
    except ValidationError as e:
        raise ValueError(f"Invalid response format: {e}")