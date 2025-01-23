from typing import Optional

import httpx

from app.jwt.dto.kakao import mapping_access_token, KakaoAccessTokenResponse, KakaoUserResponse, mapping_user_data
from app.jwt.dto.token import UserLoginInfo
from app.jwt.service.service import JWTService
from core.config.config import loader
from core.utils import Singleton


class KakaoAuthService(metaclass=Singleton):
    def __init__(self):
        self.__client_id:str = loader.config.KAKAO_CLIENT_ID
        self.__client_secret:str = loader.config.KAKAO_CLIENT_SECRET
        self.__local_redirect_uri:str = loader.config.KAKAO_LOCAL_REDIRECT_URI
        self.__prod_redirect_uri:str = loader.config.KAKAO_PROD_REDIRECT_URI
        self.__rest_api_key:str = loader.config.KAKAO_REST_API_KEY
        self.__logout_redirect_uri:str = loader.config.KAKAO_LOGOUT_REDIRECT_URI
        self.__scope: str = "profile_nickname, profile_image"
        self.__jwt_token_service = JWTService()

    def __code_auth_url(self, host: str) -> str:
        return f'https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={self.__rest_api_key}&redirect_uri={self.__get_redirect_uri(host=host)}&scope={self.__scope}'

    def __get_redirect_uri(self, host: str) -> str:
        if host == '127.0.0.1':
            return self.__local_redirect_uri
        else:
            return self.__prod_redirect_uri

    def __is_success_response(self, http_status_code: int) -> bool:
        return 200 <= http_status_code < 400

    async def do_login(self, host: str, code: str) -> UserLoginInfo:
        token : Optional[KakaoAccessTokenResponse] = await self.__get_access_token(code=code, host=host)
        if token is None:
             raise ValueError("Failed to acquire Kakao access token.")

        user_info_from_kakao: Optional[KakaoUserResponse] = await self.__get_user_info_from_kakao(access_token=token.access_token)
        if user_info_from_kakao is None:
            raise ValueError("Failed to retrieve user information from Kakao.")

        jwt_access_token = self.__jwt_token_service.create_access_token(data={"user_id": user_info_from_kakao.id})
        jwt_refresh_token = self.__jwt_token_service.create_refresh_token(data={"user_id": user_info_from_kakao.id})

        return UserLoginInfo(access_token=jwt_access_token,
                             refresh_token=jwt_refresh_token,
                             user_id=user_info_from_kakao.id, user_name=user_info_from_kakao.properties.nickname)

    async def __get_access_token(self, code:str, host: str) -> Optional[KakaoAccessTokenResponse]:
        token_request_url = 'https://kauth.kakao.com/oauth/token'
        token_request_payload = {
            "grant_type": "authorization_code",
            "client_id": self.__client_id,
            "redirect_uri": self.__get_redirect_uri(host=host),
            "code": code,
            "client_secret": self.__client_secret
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url = token_request_url, data=token_request_payload)
        return mapping_access_token(response_json=response.json()) if self.__is_success_response(response.status_code) else None

    async def __get_user_info_from_kakao(self, access_token: str) -> Optional[KakaoUserResponse]:
        userinfo_endpoint = 'https://kapi.kakao.com/v2/user/me'
        headers = {'Authorization': f'Bearer {access_token}'}

        async with httpx.AsyncClient() as client:
            response = await client.get(userinfo_endpoint, headers=headers)
        return mapping_user_data(response.json()) if self.__is_success_response(response.status_code) else None

    async def logout(self):
        logout_url = f"https://kauth.kakao.com/oauth/logout?client_id={self.__client_id}&logout_redirect_uri={self.__logout_redirect_uri}"
        async with httpx.AsyncClient() as client:
            await client.get(logout_url)

    async def reissue_access_token(self, refresh_token):
        url = "https://kauth.kakao.com/oauth/token"
        payload = {
            "grant_type": "refresh_token",
            "client_id": self.__client_id,
            "refresh_token": refresh_token
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=payload)
        access_token = response.json()
        return access_token