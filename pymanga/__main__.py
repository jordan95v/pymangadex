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
    manga_name: str,
    language: str,
    from_chapter: int | None,
    to_chapter: int | None,
    output: Path,
) -> None:
    """Download a manga from mangadex.

    Args:
        manga_name: The name of the manga to download.
        language: The language of the manga.
        from_chapter: The chapter to start downloading from.
        to_chapter: The chapter to stop downloading at.
        output: The output directory to save the manga.
    """

    client: Client = Client(base_url="https://api.mangadex.org", output=output)
    mangas: list[Manga] = await client.get_mangas(manga_name)
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
    output: Annotated[
        Path, typer.Option(help="The output directory to save the manga")
    ] = Path("output"),
) -> None:
    """Download a manga from mangadex."""

    asyncio.run(_download_manga(manga_name, language, from_chapter, to_chapter, output))


if __name__ == "__main__":
    app()  # pragma: no cover
