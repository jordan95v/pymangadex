import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Coroutine
from urllib.parse import urljoin
import httpx
from pydantic import BaseModel
from pymanga.exception import MangadexClientError
from pymanga.models.chapter import Chapter
from pymanga.models.common import Response
from pymanga.models.download_chapter_info import DownloadInfo
from pymanga.models.manga import Manga, Tag


@dataclass
class SearchTags:
    included: list[str]
    excluded: list[str]


@dataclass
class Client:
    base_url: str
    output: Path
    session: httpx.AsyncClient = httpx.AsyncClient(
        transport=httpx.AsyncHTTPTransport(retries=3)
    )

    async def _call(
        self, url: str, params: dict[str, Any], *, model: type[BaseModel]
    ) -> Response:
        """Calls the mangadex API.

        Args:
            url: The URL to concatenate with the base URL.
            model: The model to validate the response.

        Returns:
            The validated response.
        """

        full_url: str = urljoin(self.base_url, url)
        try:
            response: httpx.Response = await self.session.get(full_url, params=params)
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise MangadexClientError(e) from e
        return Response[model].model_validate(response.json())  # type: ignore

    async def get_tags(
        self, included_tags: list[str], excluded_tags: list[str]
    ) -> SearchTags:
        """Retrieves tags from the mangadex API.

        Args:
            included_tags: The list of tags to include.
            excluded_tags: The list of tags to exclude.

        Returns:
            The included and excluded tags id to be used in the search query.
        """

        response: Response[Tag] = await self._call("manga/tag", dict(), model=Tag)
        included: list[str] = [
            tag.id
            for tag in response.data
            if tag.attributes.name.get("en") in included_tags
        ]
        excluded: list[str] = [
            tag.id
            for tag in response.data
            if tag.attributes.name.get("en") in excluded_tags
        ]
        return SearchTags(included, excluded)

    async def get_mangas(
        self,
        title: str,
        tags: SearchTags | None = None,
        content_rating: list[str] | None = None,
    ) -> list[Manga]:
        """Retrieves mangas from the mangadex API.

        Args:
            title: The title of the manga.
            tags: The included and excluded tags to filter the search. Defaults to None.
            content_rating: The content rating of the manga. Defaults to None.

        Returns:
            A list of mangas that match the title and tags.
        """

        params: dict[str, Any] = {
            "title": title,
            "includedTags[]": tags.included if tags else [],
            "excludedTags[]": tags.excluded if tags else [],
        }
        if content_rating:
            params["contentRating[]"] = content_rating
        mangas: list[Manga] = []
        response: Response[Manga] = await self._call(f"/manga", params, model=Manga)
        mangas.extend(response.data)
        offset: int = response.offset + response.limit
        tasks: list[Coroutine] = []
        while response.total > offset:
            tasks.append(
                self._call(f"/manga", dict(params, offset=offset), model=Manga)
            )
            offset += response.limit
        responses: list[Response[Manga]] = await asyncio.gather(*tasks)
        for response in responses:
            mangas.extend(response.data)
        return mangas

    async def get_chapters(
        self,
        manga_id: str,
        translated_language: str,
        content_rating: list[str] | None = None,
    ) -> list[Chapter]:
        """Retrieves chapters from the mangadex API.

        Args:
            manga_id: The id of the manga.

        Returns:
            A list of chapters from the manga.
        """

        params: dict[str, Any] = {
            "manga": manga_id,
            "includeExternalUrl": 0,
            "order[chapter]": "asc",
            "translatedLanguage[]": translated_language,
        }
        if content_rating:
            params["contentRating[]"] = content_rating
        chapters: list[Chapter] = []
        response: Response[Chapter] = await self._call(
            f"/chapter", params, model=Chapter
        )
        chapters.extend(response.data)
        offset: int = response.offset + response.limit
        tasks: list[Coroutine] = []
        while response.total > offset:
            tasks.append(
                self._call(f"/chapter", dict(params, offset=offset), model=Chapter)
            )
            offset += response.limit
        responses: list[Response[Chapter]] = await asyncio.gather(*tasks)
        for response in responses:
            chapters.extend(response.data)
        return chapters

    async def get_chapter_download_info(self, chapter_id: str) -> DownloadInfo:
        """Retrieves the download information for a chapter.

        Args:
            chapter_id: The id of the chapter.

        Returns:
            The download information for the chapter.
        """

        full_url: str = urljoin(self.base_url, f"/at-home/server/{chapter_id}")
        try:
            response: httpx.Response = await self.session.get(full_url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise MangadexClientError(e) from e
        return DownloadInfo.model_validate(response.json())
