from __future__ import annotations
from pydantic import BaseModel, Field

__all__: list[str] = ["Chapter", "DownloadInfo"]


class ChapterLinks(BaseModel):
    hash: str
    data: list[str]
    data_saver: list[str] = Field(..., alias="dataSaver")


class DownloadInfo(BaseModel):
    result: str
    base_url: str = Field(..., alias="baseUrl")
    chapter: ChapterLinks
