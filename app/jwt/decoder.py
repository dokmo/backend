from abc import ABC, abstractmethod
from jose import jwt, JWTError

class AbstractJWTDecoder(ABC):
    """
    JWT 디코더 추상클래스
    decode 메소드를 구현

    :param token: JWT 토큰
    :param secret_key: JWT 암호화 키
    :param algorithm: JWT 암호화 알고리즘
    """

    @abstractmethod
    async def decode(self, token: str, secret_key: str, algorithm: str) -> dict | None:
        pass


class JWTDecoder(AbstractJWTDecoder):
    async def decode(self, token: str, secret_key: str, algorithm: str) -> dict | None:
        try:
            return jwt.decode(token, secret_key, algorithms=[algorithm])
        except JWTError:
            return None