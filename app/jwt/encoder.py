from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from jose import jwt

from core.config.config import loader

class AbstractJWTEncoder(ABC):
    """
    JWT 인코더 추상클래스
    encode 메소드를 구현

    :param data: JWT에 담을 데이터
    :param expires_delta: JWT 만료 시간
    :param secret_key: JWT 암호화 키
    :param algorithm: JWT 암호화 알고리즘
    """

    @abstractmethod
    async def encode(
            self, data: dict, expires_delta: int
    ) -> str:
        pass


class JWTEncoder(AbstractJWTEncoder):
    async def encode(
            self, data: dict, expires_delta: int
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now(ZoneInfo("Asia/Seoul")) + timedelta(minutes=expires_delta)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, key=loader.config.SECRET_KEY, algorithm=loader.config.ALGORITHM)

