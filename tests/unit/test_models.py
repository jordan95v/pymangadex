import json
from pathlib import Path
from typing import Any
import httpx
import pytest
from pytest_mock import MockerFixture
from conftest import FakeResponse
from pymanga.models.manga import Manga, Tag
from pymanga.models.chapter import Chapter
from pymanga.models.common import Response
from pymanga.models.download_chapter_info import DownloadInfo


class TestMangaModels:
    def test_manga_model(self) -> None:
        manga_json: dict[str, Any] = json.loads(
            Path("tests/samples/manga.json").read_text()
        )
        manga: Manga = Manga.model_validate(manga_json)
        assert manga.id == "6b1eb93e-473a-4ab3-9922-1a66d2a29a4a"
        assert manga.type == "manga"
        assert len(manga.relationships) == 130

    def test_chapter_model(self) -> None:
        chapter_json: dict[str, Any] = json.loads(
            Path("tests/samples/chapter.json").read_text()
        )
        chapter: Chapter = Chapter.model_validate(chapter_json)
        assert chapter.id == "176df286-1beb-47c4-81b9-aa8129a71cb5"
        assert chapter.type == "chapter"
        assert len(chapter.relationships) == 3

    def test_download_chapter_info_model(self) -> None:
        download_chapter_info_json: dict[str, Any] = json.loads(
            Path("tests/samples/download_chapter_info.json").read_text()
        )
        download_chapter_info: DownloadInfo = DownloadInfo.model_validate(
            download_chapter_info_json
        )
        assert download_chapter_info.result == "ok"
        assert download_chapter_info.base_url == "https://uploads.mangadex.org"
        assert download_chapter_info.chapter.hash == "3303dd03ac8d27452cce3f2a882e94b2"
        assert len(download_chapter_info.chapter.data) == 6
        assert len(download_chapter_info.chapter.data_saver) == 6

    @pytest.mark.asyncio
    async def test_download_chapter_info_model_download(
        self, tmp_path: Path, mocker: MockerFixture
    ) -> None:
        mocker.patch(
            "httpx.AsyncClient.get", return_value=FakeResponse(dict(), b"fake")
        )
        download_chapter_info_json: DownloadInfo = DownloadInfo.model_validate(
            json.loads(Path("tests/samples/download_chapter_info.json").read_text())
        )
        await download_chapter_info_json.download(
            tmp_path, "chapter_name", httpx.AsyncClient()
        )
        assert len(list(tmp_path.iterdir())) == 1

    @pytest.mark.parametrize(
        "json_path, model",
        [
            ("tests/samples/chapter_results.json", Chapter),
            ("tests/samples/manga_results.json", Manga),
            ("tests/samples/tag_results.json", Tag),
        ],
    )
    def test_response_model(
        self, json_path: str, model: type[Manga | Chapter | Tag]
    ) -> None:
        response_json: dict[str, Any] = json.loads(Path(json_path).read_text())
        response: Response = Response[model].model_validate(response_json)  # type: ignore
        assert isinstance(response.data[0], model)
