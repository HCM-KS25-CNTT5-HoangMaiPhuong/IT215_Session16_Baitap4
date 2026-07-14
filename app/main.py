from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import course

# Create tables if not exists
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Course Enrollment API")

# Bọc các router vào ứng dụng
app.include_router(course.router)
