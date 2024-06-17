from __future__ import annotations
from typing import Any
from pydantic import BaseModel, Field

__all__: list[str] = ["Chapter", "Attributes", "Relationship"]


class Attributes(BaseModel):
    volume: str | None = None
    chapter: str | None = None
    title: str
    translated_language: str = Field(..., alias="translatedLanguage")
    external_url: Any = Field(..., alias="externalUrl")
    publish_at: str = Field(..., alias="publishAt")
    readable_at: str = Field(..., alias="readableAt")
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt")
    pages: int
    version: int


class Relationship(BaseModel):
    id: str
    type: str


class Chapter(BaseModel):
    id: str
    type: str
    attributes: Attributes
    relationships: list[Relationship]
