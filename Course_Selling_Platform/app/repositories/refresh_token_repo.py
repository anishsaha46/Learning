from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.refresh_token import RefreshToken

class RefreshTokenRepository:
    @staticmethod
    async def create(db:AsyncSession,token:RefreshToken):
        db.add(token)
        await db.commit()
        await db.refresh(token)
        return token
    
    @staticmethod
    async def get_by_token(db:AsyncSession,token_str:str):
        stmt=select(RefreshToken).where(RefreshToken.token == token_str)
        result=await db.execute(stmt)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def revoke_token(db:AsyncSession,token:RefreshToken):
        token.revoked=True
        await db.commit()

        