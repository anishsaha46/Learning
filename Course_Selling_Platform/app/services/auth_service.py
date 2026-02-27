import datetime
from jose import jwt

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import Settings
from app.repositories.user_repo import UserRepository
from app.core.security import create_refresh_token, hash_password, verify_password, create_access_token
from app.models.user import User
from app.repositories.refresh_token_repo import RefreshTokenRepository
from app.models.refresh_token import RefreshToken


class AuthService:

    @staticmethod
    async def register(db: AsyncSession, email: str, password: str):
        existing = await UserRepository.get_by_email(db, email)

        if existing:
            raise ValueError("User already exists")

        user = User(
            email=email,
            hashed_password=hash_password(password)
        )

        return await UserRepository.create(db, user)

@staticmethod
async def login(db: AsyncSession, email: str, password: str):

    user = await UserRepository.get_by_email(db, email)

    if not user or not verify_password(password, user.hashed_password):
        raise ValueError("Invalid credentials")

    access_token = create_access_token(
        {"sub": str(user.id), "role": user.role}
    )

    refresh_token_str = create_refresh_token(
        {"sub": str(user.id)}
    )

    refresh_token = RefreshToken(
        user_id=user.id,
        token=refresh_token_str,
        expires_at=datetime.utcnow() + datetime.timedelta(
            days=Settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    )

    await RefreshTokenRepository.create(db, refresh_token)

    return access_token, refresh_token_str


@staticmethod
async def refresh(db:AsyncSession,refresh_token_str:str):

    stored_token=await RefreshTokenRepository.get_by_token(db,refresh_token_str)

    if not stored_token:
        raise ValueError("Invalid refresh token")
    
    if stored_token.revoked:
        raise ValueError("Token Revoked",401)
    
    if stored_token.expires_at < datetime.utcnow():
        raise ValueError("Refresh token expired",401)
    
    payload=jwt.decode(
        refresh_token_str,
        Settings.SECRET_KEY,
        algorithms=["HS256"]
    )

    user_id=payload.get("sub")

    await RefreshTokenRepository.revoke_token(db,stored_token)

    access_token=create_access_token({"sub":user_id})

    new_refresh_token_str=create_refresh_token({"sub":user_id})

    new_refresh_token=RefreshToken(
        user_id=user_id,
        token=new_refresh_token_str,
        expires_at=datetime.utcnow()+datetime.timedelta(days=Settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    await RefreshTokenRepository.create(db,new_refresh_token)

    return access_token,new_refresh_token_str