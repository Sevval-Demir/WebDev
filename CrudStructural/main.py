from typing import Optional, List
from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

class Course(BaseModel):
    id: int
    title: str
    instructor: str
    rating: int
    published_date: int

class CourseRequest(BaseModel):
    id: Optional[int] = Field(None, description="The ID of the course, optional")
    title: str = Field(..., min_length=3, max_length=100)
    instructor: str = Field(..., min_length=3)
    rating: int = Field(..., gt=0, lt=6)
    published_date: int = Field(..., gt=2020, lt=2100)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "My Course",
                "instructor": "Sevval Demir",
                "rating": 5,
                "published_date": 2025
            }
        }

courses_db: List[Course] = [
    Course(id=1, title="Python", instructor="Sevval", rating=5, published_date=2029),
    Course(id=2, title="Kotlin", instructor="Ahmet", rating=5, published_date=2028),
    Course(id=3, title="Jenkins", instructor="Sevval", rating=5, published_date=2027),
    Course(id=4, title="Kubernetes", instructor="Zeynep", rating=4, published_date=2026),
    Course(id=5, title="Machine Learning", instructor="Ayse", rating=1, published_date=2025),
    Course(id=6, title="Deep Learning", instructor="Fatma", rating=2, published_date=2024)
]

@app.get("/courses", response_model=List[Course], status_code=status.HTTP_200_OK)
async def get_all_courses():
    return courses_db

@app.get("/courses/{course_id}", response_model=Course, status_code=status.HTTP_200_OK)
async def get_course(course_id: int = Path(..., gt=0)):
    for course in courses_db:
        if course.id == course_id:
            return course
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

@app.get("/courses/", response_model=List[Course], status_code=status.HTTP_200_OK)
async def get_course_by_rating(course_rating: int = Query(..., gt=0, lt=6)):
    courses_to_return = [course for course in courses_db if course.rating == course_rating]
    return courses_to_return

@app.get("/courses/publish", response_model=List[Course], status_code=status.HTTP_200_OK)
async def get_course_by_publish_date(publish_date: int = Query(..., gt=2005, lt=2040)):
    courses_to_return = [course for course in courses_db if course.published_date == publish_date]
    return courses_to_return

@app.post("/create-course", response_model=Course, status_code=status.HTTP_201_CREATED)
async def create_course(course_request: CourseRequest):
    new_course = Course(
        id=find_next_course_id(),
        title=course_request.title,
        instructor=course_request.instructor,
        rating=course_request.rating,
        published_date=course_request.published_date
    )
    courses_db.append(new_course)
    return new_course

def find_next_course_id() -> int:
    return max(course.id for course in courses_db) + 1 if courses_db else 1

@app.put("/courses/update", response_model=Course, status_code=status.HTTP_200_OK)
async def update_course(course_request: CourseRequest):
    for i, course in enumerate(courses_db):
        if course.id == course_request.id:
            updated_course = Course(
                id=course_request.id,
                title=course_request.title,
                instructor=course_request.instructor,
                rating=course_request.rating,
                published_date=course_request.published_date
            )
            courses_db[i] = updated_course
            return updated_course
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

@app.delete("/courses/delete/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int = Path(..., gt=0)):
    global courses_db
    filtered_courses = [course for course in courses_db if course.id != course_id]
    if len(filtered_courses) == len(courses_db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    courses_db = filtered_courses
