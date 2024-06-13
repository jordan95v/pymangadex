import asyncio
from pathlib import Path
from typing import Annotated, Optional
import typer

from pymanga.client import Client
from pymanga.models.chapter import Chapter
from pymanga.models.download_chapter_info import DownloadInfo
from pymanga.models.manga import Manga

app: typer.Typer = typer.Typer()


async def _download_manga(
    manga_name: str, from_chapter: int | None, to_chapter: int | None
) -> None:
    client: Client = Client(base_url="https://api.mangadex.org", output=Path("output"))
    mangas: list[Manga] = await client.get_mangas(manga_name)
    print(f"Found {len(mangas)} mangas, choose one to download:")
    for i, manga in enumerate(mangas):
        print(f"{i + 1}. {manga.attributes.title['en']}")
    manga_index: int = int(input("Enter the index of the manga: ")) - 1
    choosen_manga: Manga = mangas[manga_index]
    chapters: list[Chapter] = await client.get_chapters(choosen_manga.id, "en")
    if from_chapter is not None:
        chapters = chapters[from_chapter - 1 :]
    if to_chapter is not None:
        chapters = chapters[: to_chapter - 1]
    for chapter in chapters:
        download_info: DownloadInfo = await client.get_chapter_download_info(chapter.id)
        chapter_name: str = (
            f"{chapter.attributes.chapter} - {choosen_manga.attributes.title['en']} "
            f"- {chapter.attributes.title}"
        )
        print(f"Downloading | {chapter_name}...")
        await download_info.download(client.output, chapter_name, client.session)


@app.command()
def download(
    manga_name: Annotated[
        str, typer.Argument(help="The name of the manga to download")
    ],
    from_chapter: Annotated[
        Optional[int], typer.Option(help="The chapter to start downloading from")
    ] = None,
    to_chapter: Annotated[
        Optional[int], typer.Option(help="The chapter to stop downloading at")
    ] = None,
) -> None:
    """Download a manga from MangaDex."""

    asyncio.run(_download_manga(manga_name, from_chapter, to_chapter))


if __name__ == "__main__":
    app()
