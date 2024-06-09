from dataclasses import dataclass
from pathlib import Path
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

    async def _call(self, url: str, model: type[Manga | Chapter | Tag]) -> Response:
        """Calls the MangaDex API.

        Args:
            url: The URL to concatenate with the base URL.
            model: The model to validate the response.

        Returns:
            The validated response.
        """

        full_url: str = urljoin(self.base_url, url)
        response: httpx.Response = await self.session.get(full_url)
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

        response: Response[Tag] = await self._call("manga/tag", Tag)
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
