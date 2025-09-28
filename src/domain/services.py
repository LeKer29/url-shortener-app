import hashlib
import logging
from typing import Optional
from src.domain.entities import Url
from src.application.ports.repository import UrlRepository


class UrlService:
    """
    Application service for managing shortened URLs.

    Attributes:
        repo (UrlRepository): The repository used for URL persistence.
        logger (logging.Logger): Logger instance
    """

    def __init__(self, repo: UrlRepository, logger: logging.Logger = None):
        self.repo = repo
        self.logger = logger or logging.getLogger(self.__class__.__name__)

    async def create_short_url(self, original_url: str) -> Url:
        """
        Create or retrieve a shortened URL for the given original URL.

        Args:
            original_url (str): The original full URL to shorten.

        Returns:
            Url: The persisted URL entity with the generated short code.
        """
        short_code = encode_url(original_url)

        url = await self.repo.get_by_short_code(short_code=short_code)

        if url is not None:
            self.logger.info(f"url {original_url} already exists.")
            return url

        url = await self.repo.create(original_url=original_url, short_code=short_code)

        return url

    async def get_original_url(self, short_code: str) -> Optional[str]:
        """
        Retrieve the original URL for a given short code.

        Args:
            short_code (str): The short code used to reference the original URL.

        Returns:
            Optional[str]: The original URL string if found.
        """
        url: Optional[Url] = await self.repo.get_by_short_code(short_code=short_code)

        if url is None:
            self.logger.error(
                f"An error occurred: unable to find short code {short_code}."
            )
            raise ValueError(f"Unable to find short code {short_code}")

        return url.original_url


def encode_url(url: str, short_code_size: int = 6) -> str:
    """
    Encode a URL into a short code using SHA-256 hashing.

    The hash is truncated to the given size to create a
    compact short code.

    Args:
        url (str): The URL to encode.
        short_code_size (int, optional): Length of the generated
            short code. Defaults to 6.

    Returns:
        str: The generated short code.
    """
    hash_object = hashlib.sha256(url.encode())
    return hash_object.hexdigest()[:short_code_size]
