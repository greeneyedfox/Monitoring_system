import datetime

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.db.config import settings
from sqlalchemy.future import select
from app.db.models import SystemLoad

DATABASE_URL = settings.DATABASE_URL_asyncpg

engine = create_async_engine(DATABASE_URL, future=True, echo=False)
async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db():
    async with async_session_maker() as session:
        yield session


async def record_to_db(cpu_load, ram_load, disk_load):
    async with async_session_maker() as session:
        new_record = SystemLoad(
            cpu_load=cpu_load,
            ram_load=ram_load,
            disk_load=disk_load,
            timestamp=datetime.datetime.now(),
        )
        session.add(new_record)
        await session.commit()


async def fetch_history():
    """
    Асинхронное получение данных из базы данных.
    """
    async with async_session_maker() as session:
        result = await session.execute(select(SystemLoad))
        records = result.scalars().all()
        return [
            (rec.id, rec.cpu_load, rec.ram_load, rec.disk_load, rec.timestamp)
            for rec in records
        ]
