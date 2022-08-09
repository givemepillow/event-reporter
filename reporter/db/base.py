import os

from sqlalchemy.ext.asyncio import create_async_engine

Engine = create_async_engine(
    f"postgresql+asyncpg://{os.environ['DB_URL']}",
    echo=False,
    future=True,
    pool_size=10,
    max_overflow=10
)
