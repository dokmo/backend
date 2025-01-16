from abc import ABC, abstractmethod
from jose import jwt, JWTError

from core.config.config import loader


class AbstractJWTDecoder(ABC):
    """
    JWT 디코더 추상클래스
    decode 메소드를 구현

    :param token: JWT 토큰
    :param secret_key: JWT 암호화 키
    :param algorithm: JWT 암호화 알고리즘
    """

    @abstractmethod
    def decode(self, token: str) -> dict | None:
        pass


class JWTDecoder(AbstractJWTDecoder):

    def __init__(self):
        self.__secret_key = loader.config.SECRET_KEY
        self.__algorithm = loader.config.ALGORITHM

    def decode(self, token: str) -> dict | None:
        try:
            return jwt.decode(token, self.__secret_key, algorithms=[self.__algorithm], options={"verify_exp": True})
        except JWTError:
            return None