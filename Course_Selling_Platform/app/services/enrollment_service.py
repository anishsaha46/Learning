from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.models.enrollment import Enrollment
from app.repositories.enrollment_repo import EnrollmentRepository
from app.repositories.course_repo import CourseRepository
from app.core.exceptions import AppException


class EnrollmentService:

    @staticmethod
    async def enroll(db: AsyncSession, user_id, course_id):

        #  Check course exists
        course = await CourseRepository.get_by_id(db, course_id)
        if not course:
            raise AppException("Course not found", 404)

        #  Prevent instructor enrolling in own course
        if str(course.instructor_id) == str(user_id):
            raise AppException(
                "Instructor cannot enroll in own course",
                400
            )

        enrollment = Enrollment(
            user_id=user_id,
            course_id=course_id
        )

        try:
            return await EnrollmentRepository.create(db, enrollment)

        except IntegrityError:
            # UNIQUE constraint violation
            raise AppException(
                "Already enrolled in this course",
                400
            )