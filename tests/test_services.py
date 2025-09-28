import pytest
from src.domain.services import UrlService


@pytest.mark.usefixtures("url_service", "original_url", "short_code")
class TestService:
    async def test_create_short_code(
        self, url_service: UrlService, original_url: str, short_code: str
    ):
        url = await url_service.create_short_url(original_url=original_url)

        assert url.original_url == original_url
        assert url.short_code == short_code

    async def test_create_short_code_returns_same_code_for_same_url(
        self, url_service: UrlService, original_url: str
    ):
        first_url = await url_service.create_short_url(original_url=original_url)

        second_url = await url_service.create_short_url(original_url=original_url)

        assert first_url.original_url == second_url.original_url
        assert first_url.short_code == second_url.short_code

    async def test_get_original_url_unknown_code(self, url_service: UrlService):
        short_code = "unknown-code"
        print(url_service)
        with pytest.raises(ValueError, match="Unable to find short code unknown-code"):
            await url_service.get_original_url(short_code=short_code)

    async def test_get_original_url(self, url_service: UrlService, original_url: str):
        url = await url_service.create_short_url(original_url=original_url)

        result = await url_service.get_original_url(url.short_code)

        assert result == original_url
