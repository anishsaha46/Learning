from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME:str="Course Selling API"
    DATABASE_URL:str
    DATABASE_URL_SYNC:str = None  # For Alembic migrations
    SECRET_KEY:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int=30

    REFRESH_TOKEN_EXPIRE_DAYS:int=7
    ACCESS_TOKEN_EXPIRE_MINUTES:int=30
    

    class Config:
        env_file=".env"

settings=Settings()
