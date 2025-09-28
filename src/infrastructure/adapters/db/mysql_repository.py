from typing import Optional

import aiomysql
from src.application.ports.repository import UrlRepository
from src.domain.entities import Url


class MySQLUrlRepository(UrlRepository):
    """
    MySQL-based implementation of the UrlRepository protocol.

    Attributes:
        _pool (aiomysql.Pool): The connection pool used for
            database operations.
    """

    def __init__(self, pool: aiomysql.Pool):
        self._pool = pool

    async def create(self, original_url: str, short_code: str) -> Url:
        """
        Persist a new shortened URL mapping into the database.

        Args:
            original_url (str): The original full URL to store.
            short_code (str): The unique short code to associate
                with the original URL.

        Returns:
            Url: The created URL entity.
        """
        async with self._pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    INSERT INTO urls (short_code, original_url)
                    VALUES (%s, %s)
                    """,
                    (short_code, original_url),
                )
                await conn.commit()

        return Url(original_url=original_url, short_code=short_code)

    async def get_by_short_code(self, short_code: str) -> Optional[Url]:
        """
        Retrieve a shortened URL entry by its short code.

        Args:
            short_code (str): The short code to look up.

        Returns:
            Optional[Url]: The URL entity if found, otherwise None.
        """
        async with self._pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(
                    "SELECT short_code, original_url FROM urls WHERE short_code = %s",
                    (short_code,),
                )
                row = await cur.fetchone()

        if not row:
            return None
        return Url(**row)
