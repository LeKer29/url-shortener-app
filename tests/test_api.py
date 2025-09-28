from httpx import AsyncClient
import pytest
from fastapi import status


@pytest.mark.usefixtures("test_client", "original_url", "short_code")
class TestAPI:
    async def test_create_short_code(
        self, test_client: AsyncClient, original_url: str, short_code
    ):
        response = await test_client.post(url="/urls", json={"url": original_url})

        assert response.status_code == status.HTTP_201_CREATED

        body = response.json()

        assert body["original_url"] == original_url
        assert body["short_code"] == short_code

    async def test_create_short_code_raise_validation_error(
        self, test_client: AsyncClient
    ):
        response = await test_client.post(url="/urls", json={"url": "invalid-url"})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    async def test_redirect(
        self, test_client: AsyncClient, original_url: str, short_code
    ):
        response = await test_client.post(url="/urls", json={"url": original_url})

        short_code = response.json()["short_code"]

        response = await test_client.get(f"/{short_code}", follow_redirects=False)
        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT

    async def test_redirect_raise_not_found(self, test_client: AsyncClient):
        short_code = "unknown-code"

        response = await test_client.get(f"/{short_code}", follow_redirects=False)
        assert response.status_code == status.HTTP_404_NOT_FOUND
