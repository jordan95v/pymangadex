from __future__ import annotations
import asyncio
from pathlib import Path
import shutil
import tempfile
import httpx
from pydantic import BaseModel, Field

__all__: list[str] = ["Chapter", "DownloadInfo"]


class ChapterLinks(BaseModel):
    hash: str
    data: list[str]
    data_saver: list[str] = Field(..., alias="dataSaver")


class DownloadInfo(BaseModel):
    result: str
    base_url: str = Field(..., alias="baseUrl")
    chapter: ChapterLinks

    async def _download(
        self,
        url: str,
        session: httpx.AsyncClient,
        tmp_dir: Path,
        semaphore: asyncio.Semaphore,
    ) -> None:
        """Download the image from the url and save it to the tmp_dir.

        Args:
            url (str): The url of the image to download.
            session: The httpx.AsyncClient session to use for the download.
            tmp_dir: The temporary directory to save the image.
            semaphore: The semaphore to use for the download.
        """

        async with semaphore:
            print(f"Downloading {url}")
            try:
                response: httpx.Response = await session.get(url)
                response.raise_for_status()
            except httpx.HTTPError as e:
                print(f"Failed to download {url}: {e}")
                return
            tmp_file: Path = tmp_dir / url.split("/")[-1]
            tmp_file.write_bytes(response.content)

    async def download(
        self, output: Path, chapter_name: str, session: httpx.AsyncClient
    ) -> None:
        """Downloads the chapter images and saves them as a cbz file.

        Args:
            output: The output directory to save the images.
        """

        output.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path: Path = Path(temp_dir)
            semaphore: asyncio.Semaphore = asyncio.Semaphore(5)
            await asyncio.gather(
                *[
                    self._download(
                        f"{self.base_url}/data/{self.chapter.hash}/{url}",
                        session,
                        temp_path,
                        semaphore,
                    )
                    for url in self.chapter.data
                ]
            )
            zip_path: Path = output / chapter_name
            zip_file: str = shutil.make_archive(zip_path.as_posix(), "zip", temp_dir)
            Path(zip_file).rename(zip_path.with_suffix(".cbz"))
