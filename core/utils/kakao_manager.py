import httpx
from fastapi.templating import Jinja2Templates
from core.config.config import loader


# Jinja2 템플릿 설정
templates = Jinja2Templates(directory="templates")



class KakaoAPI:
    def __init__(self):
        # 카카오 API 관련 정보를 환경 변수에서 로드
        self.client_id:str = loader.config.KAKAO_CLIENT_ID
        self.client_secret:str = loader.config.KAKAO_CLIENT_SECRET
        self.redirect_uri:str = ""
        self.local_redirect_uri:str = loader.config.KAKAO_LOCAL_REDIRECT_URI
        self.prod_redirect_uri:str = loader.config.KAKAO_PROD_REDIRECT_URI
        self.rest_api_key:str = loader.config.KAKAO_REST_API_KEY
        self.logout_redirect_uri:str = loader.config.KAKAO_LOGOUT_REDIRECT_URI

    def set_redirect_uri(self, redirect_uri):
        self.redirect_uri = redirect_uri

    def getcode_auth_url(self, scope):
        return f'https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={self.rest_api_key}&redirect_uri={self.redirect_uri}&scope={scope}'

    async def get_token(self, code:str):
        # 참고: https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api#request-token-request-body
        # 카카오로부터 인증 코드를 사용해 액세스 토큰 요청
        token_request_url = 'https://kauth.kakao.com/oauth/token'
        token_request_payload = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "code": code,
            "client_secret": self.client_secret
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url = token_request_url, data=token_request_payload)
        result = response.json()
        return result

    async def get_user_info(self, access_token):
        # 액세스 토큰을 사용하여 카카오로부터 사용자 정보 요청
        userinfo_endpoint = 'https://kapi.kakao.com/v2/user/me'
        headers = {'Authorization': f'Bearer {access_token}'}

        async with httpx.AsyncClient() as client:
            response = await client.get(userinfo_endpoint, headers=headers)
        return response.json() if response.status_code == 200 else None

    async def logout(self, client_id, logout_redirect_uri):
        # 카카오 로그아웃 URL을 호출하여 로그아웃 처리
        logout_url = f"https://kauth.kakao.com/oauth/logout?client_id={client_id}&logout_redirect_uri={logout_redirect_uri}"
        async with httpx.AsyncClient() as client:
            await client.get(logout_url)

    async def refreshAccessToken(self, clientId, refresh_token):
        # 리프레시 토큰을 사용하여 액세스 토큰 갱신 요청
        url = "https://kauth.kakao.com/oauth/token"
        payload = {
            "grant_type": "refresh_token",
            "client_id": clientId,
            "refresh_token": refresh_token
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=payload)
        refreshToken = response.json()
        return refreshToken