import json
from pathlib import Path
from typing import Any
from pymanga.models import Manga
from pymanga.models.chapter import Chapter
from pymanga.models.common import Response


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

    def test_response_model_with_chapter(self) -> None:
        response_json: dict[str, Any] = json.loads(
            Path("tests/samples/chapter_results.json").read_text()
        )
        response: Response[Chapter] = Response.model_validate(response_json)
        assert response.result == "ok"
        assert response.response == "collection"
        assert len(response.data) == 1
        assert isinstance(response.data[0], Chapter)
        assert response.limit == 10
        assert response.offset == 0
        assert response.total == 1

    def test_response_model_with_manga(self) -> None:
        response_json: dict[str, Any] = json.loads(
            Path("tests/samples/manga_results.json").read_text()
        )
        response: Response[Manga] = Response.model_validate(response_json)
        assert response.result == "ok"
        assert response.response == "collection"
        assert len(response.data) == 1
        assert isinstance(response.data[0], Manga)
        assert response.limit == 10
        assert response.offset == 0
        assert response.total == 1
