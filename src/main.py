from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.config import MySQLSettings, AppSettings
from src.infrastructure.adapters.db.mysql_pool import MySQLPool
from src.infrastructure.adapters.http.controllers import router
from src.infrastructure.logging.config import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    sql_settings = MySQLSettings()
    await MySQLPool.init_pool(sql_settings)
    yield
    await MySQLPool.close_pool()


app_settings = AppSettings()

setup_logging(level=app_settings.debug_level)

app = FastAPI(title=app_settings.name, lifespan=lifespan)

app.include_router(router)
