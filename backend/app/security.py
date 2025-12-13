from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import bcrypt
from fastapi import HTTPException, status
from jose import JWTError, jwt

from .config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica un password plano contra un hash bcrypt."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def get_password_hash(password: str) -> str:
    """Genera un hash bcrypt para el password dado."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def create_access_token(
    subject: str | int,
    expires_delta: Optional[timedelta] = None,
) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode: dict[str, Any] = {"sub": str(subject), "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return encoded_jwt


def decode_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        ) from exc


