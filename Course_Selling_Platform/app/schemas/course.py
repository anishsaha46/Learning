from pydantic import BaseModel
from decimal import Decimal


class CourseCreate(BaseModel):
    title: str
    description: str
    price: Decimal


class CourseResponse(BaseModel):
    id: str
    title: str
    description: str
    price: Decimal
    instructor_id: str

    class Config:
        from_attributes = True