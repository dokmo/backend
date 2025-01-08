from dataclasses import dataclass
from typing import TypeVar, Generic

from pydantic import BaseModel

T = TypeVar("T")

@dataclass
class DefaultResponse(BaseModel, Generic[T]):
    message: str
    data: T

    @staticmethod
    async def create_response(data: T, message: str = "OK") -> "DefaultResponse[T]":
        """
        응답 데이터를 DefaultResponse 형태로 변환하는 Static 메서드
        :param data: 응답 데이터
        :param message: 기초 메시지 (기본값: "Success")
        :return: DefaultResponse 객체
        """
        return DefaultResponse(message=message, data=data)