from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    # UUID primary key for production safety (not auto-increment)
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    role: Mapped[str] = mapped_column(
        String(50),
        default="student"  # student | instructor | admin
    )

    course=relationship("Course",back_populates="instructor",cascade="all,delete-orphan")

    enrollments=relationship("Enrollment",back_populates="user",cascade="all,delete-orphan")