from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import settings


class Base(DeclarativeBase):
    """Base declarativa para los modelos ORM."""


engine = create_async_engine(str(settings.database_url), echo=settings.debug)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db() -> AsyncSession:
    """Dependencia para obtener una sesión de BD por petición."""
    async with AsyncSessionLocal() as session:
        yield session


