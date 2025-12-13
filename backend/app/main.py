from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .db import Base, engine
from .routers import auth, products, indices
from .security import get_password_hash
from .models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(products.router)
app.include_router(indices.router)


@app.on_event("startup")
async def on_startup() -> None:
    """Crear tablas y un usuario de prueba si no existe."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Crear usuario demo
    async with AsyncSession(bind=engine, expire_on_commit=False) as session:
        result = await session.execute(
            select(User).where(User.email == "demo@toctoc.com")
        )
        user = result.scalar_one_or_none()
        if not user:
            demo_user = User(
                email="demo@toctoc.com",
                hashed_password=get_password_hash("demo1234"),
                is_active=True,
            )
            session.add(demo_user)
            await session.commit()



