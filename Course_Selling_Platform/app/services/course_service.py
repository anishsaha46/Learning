from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.course_repo import CourseRepository
from app.models.course import Course
from app.core.cache import CacheService

class CourseService:

    @staticmethod
    async def create_course(db: AsyncSession, data, instructor_id):
        course = Course(
            title=data.title,
            description=data.description,
            price=data.price,
            instructor_id=instructor_id
        )

        created= await CourseRepository.create(db, course)

        await CacheService.delete("courses:0:10")
        return created

    @staticmethod
    async def list_courses(db: AsyncSession, skip: int, limit: int):

        cache_key=f"courses:{skip}:{limit}"

        cached = await CacheService.get(cache_key)
        if cached:
            return cached
        
        courses = await CourseRepository.get_all(db,skip,limit)

        await CacheService.set(cache_key,[c.__dict__ for c in courses],ttl=60)

        return courses     

    @staticmethod
    async def get_course(db:AsyncSession,course_id):
        cache_key=f"course:{course_id}"

        cached=await CacheService.get(cache_key)
        if cached:
            return cached
        course = await CourseRepository.get_by_id(db,course_id)

        if not course:
            return None
        await CacheService.set(
            cache_key,
            course.__dict__,
            ttl=120
        )   

        return course
