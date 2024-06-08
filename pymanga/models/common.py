from typing import Generic, TypeVar
from pydantic import BaseModel

from pymanga.models import Manga
from pymanga.models.chapter import Chapter


__all__: list[str] = ["Response"]

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    result: str
    response: str
    data: list[Manga | Chapter]
    limit: int
    offset: int
    total: int
