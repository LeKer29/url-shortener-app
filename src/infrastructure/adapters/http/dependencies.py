import logging
from src.application.ports.repository import UrlRepository
from src.domain.services import UrlService
from src.infrastructure.adapters.db.mysql_pool import MySQLPool
from src.infrastructure.adapters.db.mysql_repository import MySQLUrlRepository


async def get_db_pool():
    return MySQLPool.get_pool()


async def get_repository() -> UrlRepository:
    pool = await get_db_pool()
    return MySQLUrlRepository(pool)


async def get_url_service() -> UrlService:
    logger = logging.getLogger("UrlService")

    repo = await get_repository()
    return UrlService(repo, logger)
