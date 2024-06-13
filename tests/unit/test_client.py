import json
from pathlib import Path
from typing import Any
import pytest
from pytest_mock import MockerFixture
from conftest import FakeResponse
from pymanga.client import Client, SearchTags
from pymanga.models.chapter import Chapter
from pymanga.models.common import Response
from pymanga.models.manga import Manga, Tag


@pytest.mark.asyncio
class TestClient:
    @pytest.mark.parametrize(
        "json_path, model",
        [
            ("tests/samples/chapter_results.json", Chapter),
            ("tests/samples/manga_results.json", Manga),
            ("tests/samples/tag_results.json", Tag),
        ],
    )
    async def test__call(
        self,
        client: Client,
        mocker: MockerFixture,
        json_path: str,
        model: type[Manga | Chapter | Tag],
    ) -> None:
        json_data: dict[str, Any] = json.loads(Path(json_path).read_text())
        mocker.patch.object(client.session, "get", return_value=FakeResponse(json_data))
        result: Response = await client._call("any", dict(), model=model)
        assert isinstance(result, Response)
        assert isinstance(result.data[0], model)

    async def test_get_tags(self, client: Client, mocker: MockerFixture) -> None:
        response: Response[Tag] = Response[Tag].model_validate(
            json.loads(Path("tests/samples/tag_results.json").read_text())
        )
        mocker.patch.object(client, "_call", return_value=response)
        tags: SearchTags = await client.get_tags(
            included_tags=["Oneshot"], excluded_tags=["Military"]
        )
        assert tags.included == ["0234a31e-a729-4e28-9d6a-3f87c4966b9e"]
        assert tags.excluded == ["ac72833b-c4e9-4878-b9db-6c8a4a99444a"]

    async def test_get_mangas(self, client: Client, mocker: MockerFixture) -> None:
        first_response: Response[Manga] = Response[Manga].model_validate(
            json.loads(Path("tests/samples/manga_results.json").read_text())
        )
        second_response: Response[Manga] = Response[Manga].model_validate(
            json.loads(Path("tests/samples/manga_second_results.json").read_text())
        )
        mocker.patch.object(
            client, "_call", side_effect=[first_response, second_response]
        )
        mangas: list[Manga] = await client.get_mangas(
            "Jujutsu Kaisen offered me some a+ combat in s2"
        )
        assert len(mangas) == 2

    async def test_get_chapters(self, client: Client, mocker: MockerFixture) -> None:
        first_response: Response[Chapter] = Response[Chapter].model_validate(
            json.loads(Path("tests/samples/chapter_results.json").read_text())
        )
        second_response: Response[Chapter] = Response[Chapter].model_validate(
            json.loads(Path("tests/samples/chapter_second_results.json").read_text())
        )
        mocker.patch.object(
            client, "_call", side_effect=[first_response, second_response]
        )
        chapters: list[Chapter] = await client.get_chapters(
            "Jujutsu Kaisen offered me some a+ combat in s2", "en"
        )
        assert len(chapters) == 2
