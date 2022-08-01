import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(create_async_engine(
    f"postgresql+asyncpg://{os.environ['DB_URL']}",
    echo=False,
    future=True,
    pool_size=10,
    max_overflow=10
), expire_on_commit=False, class_=AsyncSession)
