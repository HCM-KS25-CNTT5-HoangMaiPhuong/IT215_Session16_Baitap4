from pydantic import BaseModel, EmailStr
from typing import List

class StudentBase(BaseModel):
    id: int
    full_name: str
    email: EmailStr

class CourseStudentListResponse(BaseModel):
    course_id: int
    course_name: str
    total_students: int
    students: List[StudentBase]

class Config:
    from_attributes = True
