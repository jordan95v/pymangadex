from __future__ import annotations
from typing import Any
from pydantic import BaseModel, Field

__all__: list[str] = [
    "Description",
    "Links",
    "TagAttributes",
    "Tag",
    "Attributes",
    "Relationship",
    "Manga",
]


class Description(BaseModel):
    bg: str | None = None
    cs: str | None = None
    de: str | None = None
    en: str | None = None
    es: str | None = None
    fi: str | None = None
    fr: str | None = None
    id: str | None = None
    it: str | None = None
    ja: str | None = None
    pl: str | None = None
    pt: str | None = None
    ru: str | None = None
    sr: str | None = None
    tr: str | None = None
    pt_br: str | None = Field(None, alias="pt-br")
    uk: str | None = None
    ar: str | None = None


class Links(BaseModel):
    al: str | None = None
    ap: str | None = None
    bw: str | None = None
    kt: str | None = None
    mu: str | None = None
    amz: str | None = None
    ebj: str | None = None
    mal: str | None = None
    raw: str | None = None
    engtl: str | None = None


class TagAttributes(BaseModel):
    name: dict[str, str]
    description: dict[str, Any]
    group: str
    version: int


class Tag(BaseModel):
    id: str
    type: str
    attributes: TagAttributes
    relationships: list[Relationship]


class Attributes(BaseModel):
    title: dict[str, str]
    alt_titles: list[dict[str, str]] = Field(..., alias="altTitles")
    description: Description
    is_locked: bool = Field(..., alias="isLocked")
    links: Links
    original_language: str = Field(..., alias="originalLanguage")
    last_volume: str = Field(..., alias="lastVolume")
    last_chapter: str = Field(..., alias="lastChapter")
    publication_demographic: str | None = Field(..., alias="publicationDemographic")
    status: str
    year: int
    content_rating: str = Field(..., alias="contentRating")
    tags: list[Tag]
    state: str
    chapter_numbers_reset_on_new_volume: bool = Field(
        ..., alias="chapterNumbersResetOnNewVolume"
    )
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt")
    version: int
    available_translated_languages: list[str] = Field(
        ..., alias="availableTranslatedLanguages"
    )
    latest_uploaded_chapter: str = Field(..., alias="latestUploadedChapter")


class Relationship(BaseModel):
    id: str
    type: str
    related: str | None = None


class Manga(BaseModel):
    id: str
    type: str
    attributes: Attributes
    relationships: list[Relationship]
