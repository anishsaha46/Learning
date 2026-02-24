from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repo import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User


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

        if not user:
            raise ValueError("Invalid credentials")

        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        token = create_access_token(
            {"sub": str(user.id), "role": user.role}
        )

        return token