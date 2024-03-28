import logging
from tortoise import Tortoise
from tortoise.transactions import in_transaction

from app.utils.settings import settings

logger = logging.getLogger(__name__)


async def init_db():
    print("I AM HERE!")
    try:
        await Tortoise.init(
            db_url=f'postgres://postgres:{settings.POSTGRES_PASSWORD}@postgres:5432/{settings.POSTGRES_DB}',
            modules={'models': ['app.db.videos']},
        )
        logger.info("Tortoise ORM initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing Tortoise ORM: {e}")
        raise

    try:
        await Tortoise.generate_schemas()
        logger.info("Tortoise ORM schemas generated successfully")
        await create_full_text_index()
    except Exception as e:
        logger.error(f"Error generating Tortoise ORM schemas: {e}")
        raise


async def create_full_text_index():
    async with in_transaction() as conn:
        await conn.execute_script(
            f"CREATE INDEX IF NOT EXISTS videos_title_full_text_idx ON videos USING gin(to_tsvector('english', title));"
        )


async def startup():
    await init_db()


async def shutdown():
    await Tortoise.close_connections()
