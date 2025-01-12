import pytest
import pytest_asyncio
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.db.database import record_to_db, fetch_history


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def setup_test_db():
    # Здесь должна быть тестовая бд, но я использую основную
    TEST_DATABASE_URL = "postgresql+asyncpg://user:123@localhost:5432/mydb"
    test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)

    TestSessionLocal = sessionmaker(
        bind=test_engine, expire_on_commit=False, class_=AsyncSession
    )

    yield (TestSessionLocal, test_engine)

    await test_engine.dispose()


@pytest.mark.asyncio
async def test_record_and_fetch_history(setup_test_db, monkeypatch):
    TestSessionLocal, test_engine = setup_test_db

    def _fake_sessionmaker():
        return TestSessionLocal()

    monkeypatch.setattr("app.db.database.async_session_maker", _fake_sessionmaker)

    # Пишем данные
    await record_to_db(cpu_load=10, ram_load=100, disk_load=1000)
    await record_to_db(cpu_load=20, ram_load=200, disk_load=2000)

    # Читаем
    results = await fetch_history()
    assert len(results) >= 1  # т.к. в базе есть записи от запуска приложения

    # Проверяем последние 2 записи
    last1 = results[-2]
    last2 = results[-1]

    assert last1[1] == 10
    assert last1[2] == 100
    assert last1[3] == 1000

    assert last2[1] == 20
    assert last2[2] == 200
    assert last2[3] == 2000
