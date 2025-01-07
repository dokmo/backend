from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from jose import jwt, ExpiredSignatureError
from core.config.config import loader


class JWTService:
    """
    JWT 로그인시 access token, refresh token을 생성하는 로직
    """

    def __init__(
            self,
            algorithm: str = loader.config.ALGORITHM,
            secret_key: str = loader.config.SECRET_KEY,
            access_token_expire_time: int = loader.config.ACCESS_TOKEN_EXPIRE_MINUTES,
            refresh_token_expire_time: int = loader.config.REFRESH_TOKEN_EXPIRE_MINUTES,
    ):
        self.algorithm = algorithm
        self.secret_key = secret_key
        self.access_token_expire_time = access_token_expire_time
        self.refresh_token_expire_time = refresh_token_expire_time


    async def create_access_token(self, data: dict) -> str:
        return await self._create_token(data, self.access_token_expire_time)

    async def create_refresh_token(self, data: dict) -> str:
        return await self._create_token(data, self.refresh_token_expire_time)

    async def _create_token(self, data: dict, expires_delta: int) -> str:
        to_encode = data.copy()
        expire = datetime.now(ZoneInfo("Asia/Seoul")) + timedelta(minutes=expires_delta)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, key = self.secret_key, algorithm = self.algorithm) # 암호화 및 토큰 생성
        return encoded_jwt

    # middlewares의 auth가 역할을 대신함.
    async def check_token_expired(self, token: str) -> dict | None:
        try:
            decoded_data = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return decoded_data
        except Exception as e:
            print("Token verification failed:", e)
            return None


if __name__ == "__main__":
    jwt_service = JWTService()
    token = jwt_service.create_access_token({"sub": "user@example.com"})
    print(token)

