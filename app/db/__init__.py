from tortoise import Tortoise
from tortoise.transactions import in_transaction

from app.utils.settings import settings


async def init_db():
    await Tortoise.init(
        db_url=f'postgres://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@postgres:5432/{settings.POSTGRES_DB}',
        modules={'models': ['app.db.videos']},
    )
    await Tortoise.generate_schemas()
    await create_full_text_index()


async def create_full_text_index():
    async with in_transaction() as conn:
        await conn.execute_script(
            f"CREATE INDEX IF NOT EXISTS videos_title_description_full_text_idx "
            f"ON videos USING gin(to_tsvector('english', coalesce(title, '') || ' ' || coalesce(description, '')));"
        )


async def startup():
    await init_db()


async def shutdown():
    await Tortoise.close_connections()
