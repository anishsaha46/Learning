from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
from fastapi import Depends, HTTPException,status
from app.core.config import settings

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token:str=Depends(oauth2_scheme)):
    try:
        paylaod=jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )
        return paylaod
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )