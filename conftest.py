from dataclasses import dataclass
from pathlib import Path
import pytest
from pymanga.client import Client


@pytest.fixture
def client() -> Client:
    return Client(
        base_url="https://api.mangadex.org",
        output=Path("tests/output"),
    )


@dataclass
class FakeResponse:
    json_data: dict[str, str]
    content: bytes

    def json(self) -> dict[str, str]:
        return self.json_data

    def raise_for_status(self) -> None:
        pass
