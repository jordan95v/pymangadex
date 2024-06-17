import asyncio
from pathlib import Path
from typing import Annotated, Optional
import typer
from pymanga.client import Client, SearchTags
from pymanga.models.chapter import Chapter
from pymanga.models.download_chapter_info import DownloadInfo
from pymanga.models.manga import Manga

app: typer.Typer = typer.Typer()


async def _download_manga(
    manga_name: str,
    language: str,
    from_chapter: int | None,
    to_chapter: int | None,
    included_tags: list[str],
    excluded_tags: list[str],
    content_rating: list[str],
    output: Path,
) -> None:
    """Download a manga from mangadex.

    Args:
        manga_name: The name of the manga to download.
        language: The language of the manga.
        from_chapter: The chapter to start downloading from.
        to_chapter: The chapter to stop downloading at.
        included_tags: The tags to include in the search query.
        excluded_tags: The tags to exclude in the search query.
        content_rating: The content rating of the manga.
        output: The output directory to save the manga.
    """

    client: Client = Client(base_url="https://api.mangadex.org", output=output)
    search_tags: SearchTags | None = None
    if len(included_tags) or len(excluded_tags):
        search_tags = await client.get_tags(included_tags, excluded_tags)
    mangas: list[Manga] = await client.get_mangas(
        manga_name, search_tags, content_rating
    )
    if not mangas:
        print("No mangas found.")
        return
    print(f"Found {len(mangas)} mangas, choose one to download:")
    for i, manga in enumerate(mangas):
        print(f"{i + 1}. {manga.attributes.title['en']}")
    try:
        manga_index: int = int(input("Enter the index of the manga: ")) - 1
        choosen_manga: Manga = mangas[manga_index]
    except ValueError:
        print("Invalid input, please enter a number.")
        return
    except IndexError:
        print("Invalid index, please enter a valid index.")
        return
    chapters: list[Chapter] = await client.get_chapters(choosen_manga.id, language)
    if from_chapter is not None:
        chapters = chapters[from_chapter - 1 :]
    if to_chapter is not None:
        chapters = chapters[: to_chapter - 1]
    for chapter in chapters:
        download_info: DownloadInfo = await client.get_chapter_download_info(chapter.id)
        chapter_name: str = (
            f"{chapter.attributes.chapter} - {choosen_manga.attributes.title['en']}"
            f" -{chapter.attributes.title}"
        )
        print(f"Downloading | {chapter_name}...")
        await download_info.download(client.output, chapter_name, client.session)


@app.command()
def download(
    manga_name: Annotated[
        str, typer.Argument(help="The name of the manga to download")
    ],
    language: Annotated[str, typer.Option(help="The language of the manga")] = "en",
    from_chapter: Annotated[
        Optional[int], typer.Option(help="The chapter to start downloading from")
    ] = None,
    to_chapter: Annotated[
        Optional[int], typer.Option(help="The chapter to stop downloading at")
    ] = None,
    included_tags: Annotated[
        Optional[str], typer.Option(help="The tags to include in the search query")
    ] = "",
    excluded_tags: Annotated[
        Optional[str], typer.Option(help="The tags to exclude in the search query")
    ] = "",
    content_rating: Annotated[
        Optional[str], typer.Option(help="The content rating of the manga")
    ] = "",
    output: Annotated[
        Path, typer.Option(help="The output directory to save the manga")
    ] = Path("output"),
) -> None:
    """Download a manga from mangadex."""

    asyncio.run(
        _download_manga(
            manga_name,
            language,
            from_chapter,
            to_chapter,
            included_tags.split(",") if included_tags else [],
            excluded_tags.split(",") if excluded_tags else [],
            content_rating.split(",") if content_rating else [],
            output,
        )
    )


if __name__ == "__main__":
    app()  # pragma: no cover
