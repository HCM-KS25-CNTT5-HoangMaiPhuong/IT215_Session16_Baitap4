from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/{course_id}/students", response_model=schemas.CourseStudentListResponse)
def get_course_students(course_id: int, db: Session = Depends(get_db)):
    # 1. Kiểm tra khóa học tồn tại
    course = db.scalars(select(models.Course).where(models.Course.id == course_id)).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Khóa học không tồn tại"
        )
    
    # 2. Sử dụng JOIN để lấy danh sách sinh viên
    stmt = (
        select(models.Student)
        .join(models.Enrollment, models.Student.id == models.Enrollment.student_id)
        .where(
            models.Enrollment.course_id == course_id,
            models.Enrollment.status.in_(["STUDYING", "COMPLETED"]),
            models.Student.status == "ACTIVE"
        )
        .distinct()
        .order_by(models.Student.full_name)
    )
    
    students = db.scalars(stmt).all()
    
    # 3. Format đầu ra
    students_list = [
        schemas.StudentBase(id=s.id, full_name=s.full_name, email=s.email)
        for s in students
    ]
    
    return schemas.CourseStudentListResponse(
        course_id=course.id,
        course_name=course.name,
        total_students=len(students_list),
        students=students_list
    )
