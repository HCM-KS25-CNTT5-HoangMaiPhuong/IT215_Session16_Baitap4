from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    status = Column(String(50), nullable=False, default="ACTIVE")  # ACTIVE / INACTIVE

    enrollments = relationship("Enrollment", back_populates="student")

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="OPEN")  # OPEN / CLOSED

    enrollments = relationship("Enrollment", back_populates="course")

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    status = Column(String(50), nullable=False)  # STUDYING, CANCELLED, COMPLETED

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
