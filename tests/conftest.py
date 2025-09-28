import asyncio
import logging
from typing import Optional

from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
import pytest
from src.domain.entities import Url
from src.main import app
from src.application.ports.repository import UrlRepository
from src.domain.services import UrlService
from src.infrastructure.adapters.http.dependencies import get_url_service


class FakeRepository(UrlRepository):
    def __init__(self):
        self.storage = {}

    async def create(self, original_url: str, short_code: str) -> Url:  # <-- async
        self.storage[short_code] = Url(original_url=original_url, short_code=short_code)
        return self.storage[short_code]

    async def get_by_short_code(self, short_code: str) -> Optional[Url]:  # <-- async
        return self.storage.get(short_code)


@pytest.fixture(scope="session")
def event_loop():
    """Ensure a single event loop for async tests."""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def fake_repo():
    return FakeRepository()


@pytest.fixture
async def url_service(fake_repo):
    logger = logging.getLogger("test")
    logger.addHandler(logging.NullHandler())
    return UrlService(fake_repo)


@pytest.fixture
def original_url() -> str:
    return "https://dummy-url.com/"


@pytest.fixture
def short_code() -> str:
    return "493d4c"


@pytest.fixture
async def test_client(fake_repo) -> TestClient:
    app.dependency_overrides = {}
    app.dependency_overrides[get_url_service] = lambda: UrlService(fake_repo)

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
