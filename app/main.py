from fastapi import FastAPI
from .api import router as students_router


app = FastAPI(title="Student Marks API")

app.include_router(students_router)

@app.get("/")
def root():
    return {"message": "Welcome to the Student Marks API"}


