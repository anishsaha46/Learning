from sqlalchemy.orm import DeclarativeBase

# Central Base class for all ORM models
class Base(DeclarativeBase):
    pass


# Import all models here so Alembic can detect them
from app.models.user import User
from app.models.course import Course
from app.models.enrollment import Enrollment
