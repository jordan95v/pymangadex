import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock
import pytest
from pytest_mock import MockerFixture
from pymanga.__main__ import download, _download_manga
from pymanga.client import Client, SearchTags
from pymanga.models.chapter import Chapter
from pymanga.models.common import Response
from pymanga.models.download_chapter_info import DownloadInfo
from pymanga.models.manga import Manga


class TestCommands:
    def test_download(self, mocker: MockerFixture) -> None:
        download_mock: MagicMock = mocker.patch("pymanga.__main__._download_manga")
        download("Jujustu Kaisen")
        download_mock.assert_called_once_with(
            "Jujustu Kaisen", "en", None, None, [], [], [], Path("./output")
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "input_value, expected_call_count, from_chapter, to_chapter",
        [
            ("1", 1, None, None),
            ("1", 1, 1, None),
            ("1", 0, 2, 1),
            ("fake", 0, None, None),
            ("2", 0, None, None),
        ],
    )
    async def test__download_manga(
        self,
        mocker: MockerFixture,
        input_value: str,
        expected_call_count: int,
        from_chapter: int,
        to_chapter: int,
    ) -> None:
        mangas_json: dict[str, Any] = json.loads(
            Path("tests/samples/manga_results.json").read_text()
        )
        chapters_json: dict[str, Any] = json.loads(
            Path("tests/samples/chapter_results.json").read_text()
        )
        download_json: dict[str, Any] = json.loads(
            Path("tests/samples/download_chapter_info.json").read_text()
        )
        mangas: list[Manga] = Response[Manga].model_validate(mangas_json).data
        chapters: list[Chapter] = Response[Chapter].model_validate(chapters_json).data
        download: DownloadInfo = DownloadInfo.model_validate(download_json)
        mocker.patch.object(Client, "get_mangas", return_value=mangas)
        mocker.patch.object(Client, "get_chapters", return_value=chapters)
        mocker.patch.object(Client, "get_chapter_download_info", return_value=download)
        get_tags_mock: MagicMock = mocker.patch.object(
            Client,
            "get_tags",
            return_value=SearchTags(included=["shounen", "action"], excluded=["yaoi"]),
        )
        mocker.patch("builtins.input", return_value=input_value)
        download_mock: MagicMock = mocker.patch.object(DownloadInfo, "download")
        await _download_manga(
            "Jujustu Kaisen", "en", from_chapter, to_chapter, [], [], [], Path("output")
        )
        assert download_mock.call_count == expected_call_count
        get_tags_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_download_manga_with_tags(self, mocker: MockerFixture) -> None:
        mangas_json: dict[str, Any] = json.loads(
            Path("tests/samples/manga_results.json").read_text()
        )
        chapters_json: dict[str, Any] = json.loads(
            Path("tests/samples/chapter_results.json").read_text()
        )
        download_json: dict[str, Any] = json.loads(
            Path("tests/samples/download_chapter_info.json").read_text()
        )
        mangas: list[Manga] = Response[Manga].model_validate(mangas_json).data
        chapters: list[Chapter] = Response[Chapter].model_validate(chapters_json).data
        download: DownloadInfo = DownloadInfo.model_validate(download_json)
        mocker.patch.object(Client, "get_mangas", return_value=mangas)
        mocker.patch.object(Client, "get_chapters", return_value=chapters)
        mocker.patch.object(Client, "get_chapter_download_info", return_value=download)
        get_tags_mock: MagicMock = mocker.patch.object(
            Client,
            "get_tags",
            return_value=SearchTags(included=["shounen", "action"], excluded=["yaoi"]),
        )
        mocker.patch("builtins.input", return_value="1")
        download_mock: MagicMock = mocker.patch.object(DownloadInfo, "download")
        await _download_manga(
            "Jujustu Kaisen",
            "en",
            None,
            None,
            ["shounen", "action"],
            ["yaoi"],
            ["safe", "suggestive"],
            Path("output"),
        )
        get_tags_mock.assert_called_once()
        download_mock.assert_called_once()
