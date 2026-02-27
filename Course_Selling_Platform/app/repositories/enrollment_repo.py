from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.models.enrollment import Enrollment


class EnrollmentRepository:

    @staticmethod
    async def create(db: AsyncSession, enrollment: Enrollment):
        try:
            db.add(enrollment)
            await db.commit()
            await db.refresh(enrollment)
            return enrollment

        except IntegrityError:
            # Rollback is mandatory after failed commit
            await db.rollback()
            raise

    @staticmethod
    async def get_by_user_and_course(
        db: AsyncSession,
        user_id,
        course_id
    ):
        stmt = select(Enrollment).where(
            Enrollment.user_id == user_id,
            Enrollment.course_id == course_id
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()