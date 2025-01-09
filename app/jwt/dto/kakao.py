from dataclasses import dataclass

from pydantic import BaseModel, ValidationError


@dataclass
class KakaoUserData(BaseModel):
    id: int
    nickname: str

@dataclass
class KakaoAccessTokenResponse(BaseModel):
    token_type: str
    access_token: str
    id_token: str
    expires_in: int
    refresh_token: str
    refresh_token_expires_in: int
    scope: str

@dataclass
class KakaoProperties(BaseModel):
    nickname: str
    profile_image: str
    thumbnail_image: str

@dataclass
class KakaoUserResponse(BaseModel):
    id: int
    properties: KakaoProperties


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