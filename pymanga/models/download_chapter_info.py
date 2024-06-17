from __future__ import annotations
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
            for url in self.chapter.data:
                full_url: str = f"{self.base_url}/data/{self.chapter.hash}/{url}"
                response: httpx.Response = await session.get(full_url)
                tmp_file: Path = temp_path / url.split("/")[-1]
                tmp_file.write_bytes(response.content)
            zip_path: Path = output / chapter_name
            zip_file: str = shutil.make_archive(zip_path.as_posix(), "zip", temp_dir)
            Path(zip_file).rename(zip_path.with_suffix(".cbz"))
