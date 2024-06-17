from typing import Generic, TypeVar
from pydantic import BaseModel

__all__: list[str] = ["Response"]

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    result: str
    response: str
    data: list[T]
    limit: int
    offset: int
    total: int
