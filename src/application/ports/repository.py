from typing import Protocol, Optional
from src.domain.entities import Url


class UrlRepository(Protocol):
    """
    Url repository contract

    Methods
    -------
    create(original_url: str, short_code: str) -> Url
        Create the `Url` entity

    get_by_short_code(short_code: str) -> Optional[Url]
        Retrieve the `Url` entity associated with the given
        short code. Returns `None` if the short code does not
        exist in the repository.
    """

    async def create(self, original_url: str, short_code: str) -> Url:
        raise NotImplementedError

    async def get_by_short_code(self, short_code: str) -> Optional[Url]:
        raise NotImplementedError
