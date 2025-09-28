import aiomysql
from typing import Optional
from src.config import MySQLSettings


class MySQLPool:
    """
    Asynchronous connection pool manager for MySQL.

    Attributes:
        _pool (Optional[aiomysql.Pool]): The underlying connection pool.
        _settings (Optional[MySQLSettings]): Settings used to configure the pool.
    """

    _pool: Optional[aiomysql.Pool] = None
    _settings: Optional[MySQLSettings] = None

    @classmethod
    async def init_pool(cls, settings: MySQLSettings | None = None) -> None:
        """
        Initialize the MySQL connection pool.

        Args:
            settings (MySQLSettings | None, optional): Custom MySQL
                configuration. If not provided, defaults from
                `MySQLSettings` will be used.
        """
        if cls._pool is not None:
            return

        cls._settings = settings or MySQLSettings()

        cls._pool = await aiomysql.create_pool(
            host=cls._settings.host,
            port=cls._settings.port,
            user=cls._settings.user,
            password=cls._settings.password,
            db=cls._settings.database,
            minsize=cls._settings.pool_min,
            maxsize=cls._settings.pool_max,
            autocommit=True,
            charset="utf8mb4",
        )

    @classmethod
    def get_pool(cls) -> aiomysql.Pool:
        """
        Get the active MySQL connection pool.

        Returns:
            aiomysql.Pool: The initialized connection pool.
        """
        if cls._pool is None:
            raise RuntimeError(
                "MySQL pool has not been initialized. Call init_pool() first."
            )
        return cls._pool

    @classmethod
    async def close_pool(cls) -> None:
        """
        Close the MySQL connection pool.
        """
        if cls._pool:
            cls._pool.close()
            await cls._pool.wait_closed()
            cls._pool = None
