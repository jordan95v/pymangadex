import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Coroutine
from urllib.parse import urljoin
import httpx
from pymanga.models.chapter import Chapter
from pymanga.models.common import Response
from pymanga.models.manga import Manga, Tag


@dataclass
class SearchTags:
    included: list[str]
    excluded: list[str]


@dataclass
class Client:
    base_url: str
    output: Path
    session: httpx.AsyncClient = httpx.AsyncClient()

    async def _call(
        self, url: str, params: dict[str, Any], *, model: type[Manga | Chapter | Tag]
    ) -> Response:
        """Calls the MangaDex API.

        Args:
            url: The URL to concatenate with the base URL.
            model: The model to validate the response.

        Returns:
            The validated response.
        """

        full_url: str = urljoin(self.base_url, url)
        response: httpx.Response = await self.session.get(full_url, params=params)
        response.raise_for_status()
        return Response[model].model_validate(response.json())  # type: ignore

    async def get_tags(
        self, included_tags: list[str], excluded_tags: list[str]
    ) -> SearchTags:
        """Retrieves tags from the MangaDex API.

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
        self, title: str, tags: SearchTags | None = None
    ) -> list[Manga]:
        """Retrieves mangas from the MangaDex API.

        Args:
            title: The title of the manga.
            tags: The included and excluded tags to filter the search. Defaults to None.

        Returns:
            A list of mangas that match the title and tags.
        """

        params: dict[str, Any] = {
            "title": title,
            "includedTags[]": tags.included if tags else [],
            "excludedTags[]": tags.excluded if tags else [],
        }
        mangas: list[Manga] = []
        response: Response[Manga] = await self._call(f"/manga", params, model=Manga)
        mangas.extend(response.data)
        offset: int = response.offset + response.limit
        tasks: list[Coroutine] = []
        while response.total > offset:
            new_params: dict[str, Any] = params.copy()
            tasks.append(self._call(f"/manga", new_params, model=Manga))
            offset += response.limit
        responses: list[Response[Manga]] = await asyncio.gather(*tasks)
        for response in responses:
            mangas.extend(response.data)
        return mangas

    async def get_chapters(
        self, manga_id: str, translated_language: str
    ) -> list[Chapter]:
        """Retrieves chapters from the MangaDex API.

        Args:
            manga_id: The id of the manga.

        Returns:
            A list of chapters from the manga.
        """

        params: dict[str, Any] = {
            "manga": manga_id,
            "translatedLanguage[]": translated_language,
        }
        chapters: list[Chapter] = []
        response: Response[Chapter] = await self._call(
            f"/chapter", params, model=Chapter
        )
        chapters.extend(response.data)
        offset: int = response.offset + response.limit
        tasks: list[Coroutine] = []
        while response.total > offset:
            new_params: dict[str, Any] = params.copy()
            tasks.append(self._call(f"/chapter", new_params, model=Chapter))
            offset += response.limit
        responses: list[Response[Chapter]] = await asyncio.gather(*tasks)
        for response in responses:
            chapters.extend(response.data)
        return chapters
