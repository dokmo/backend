from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from jose import jwt, ExpiredSignatureError
from core.config.config import loader
from core.utils import Singleton


class JWTService(metaclass=Singleton):
    """
    JWT 로그인시 access token, refresh token을 생성하는 로직
    """

    def __init__(
            self,
            algorithm: str = loader.config.ALGORITHM,
            secret_key: str = loader.config.SECRET_KEY,
            access_token_expire_time: int = int(loader.config.ACCESS_TOKEN_EXPIRE_MINUTES),
            refresh_token_expire_time: int = int(loader.config.REFRESH_TOKEN_EXPIRE_MINUTES),
    ):
        self.__algorithm = algorithm
        self.__secret_key = secret_key
        self.__access_token_expire_time = access_token_expire_time
        self.__refresh_token_expire_time = refresh_token_expire_time


    def create_access_token(self, data: dict) -> str:
        return self.__create_token(data, self.__access_token_expire_time)

    def create_refresh_token(self, data: dict) -> str:
        return self.__create_token(data, self.__refresh_token_expire_time)

    def __create_token(self, data: dict, expires_delta: int) -> str:
        to_encode = data.copy()
        expire = datetime.now(ZoneInfo("Asia/Seoul")) + timedelta(minutes=expires_delta)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, key = self.__secret_key, algorithm = self.__algorithm) # 암호화 및 토큰 생성
        return encoded_jwt

    # middlewares의 auth가 역할을 대신함.
    async def check_token_expired(self, token: str) -> dict | None:
        try:
            decoded_data = jwt.decode(token, self.__secret_key, algorithms=[self.__algorithm])
            return decoded_data
        except Exception as e:
            print("Token verification failed:", e)
            return None
