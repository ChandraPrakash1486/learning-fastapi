from fastapi import APIRouter, Query, Path, HTTPException, status, Depends
from .schemas import SearchField, SearchResponse, StudentCreate, StudentCreatePatch, UserLogin
from . import services, auth

router = APIRouter(prefix="/student_marks", tags=["Students"])

@router.get("/search/{search_field}/{search_value}", response_model=SearchResponse)
def search_students(
    search_field: SearchField = Path(...), 
    search_value: str = Path(...), 
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    student_marks = services.load_students_marks_data()
    all_students = list(student_marks)
    
    try:    
        filtered_students = services.filter_students_marks_data_by_field(all_students, search_field, search_value)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not filtered_students:
        raise HTTPException(status_code=404, detail="No students found matching the criteria")

    paginated_results = filtered_students[offset:offset + limit]
    
    return {
    "metadata": {
        "searched_by": search_field.value,
        "searched_value": search_value
    },
    "pagination": {
        "total_matches": len(filtered_students),
        "showing": len(paginated_results),
        "offset": offset,
        "limit": limit
    },
    "results": paginated_results
}


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_student(new_student_data: StudentCreate):
    saved_student_data = services.create_student(new_student_data)
    return {
        "message": "Student created successfully",
        "student": saved_student_data
    }
    
@router.put("/{student_id}")
def update_student_put(student_data: StudentCreate, student_id: int = Path(..., ge=1)):
    updated_student_data = services.update_student_full_data(student_id, student_data)
    return {
        "message": "Student updated successfully",
        "student": updated_student_data
    }

@router.patch("/{student_id}")
def update_student_patch(student_id: int = Path(..., ge=1), student_data: StudentCreatePatch = None):
    updated_student_data = services.update_student_partial_data(student_id, student_data)
    return {
        "message": "Student updated successfully",
        "student": updated_student_data
    }



@router.post("/login", tags=["Security"])
def login_for_access_token(user_data: UserLogin):
    users = auth.load_users()

    
    if user_data.username not in users or users[user_data.username]["password"] != user_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    # Generate a fake token for demonstration
    fake_token = f"{user_data.username}-secret-token"
    
    return {
        "access_token": fake_token, 
        "token_type": "bearer"
    }


#--------------------Secure DELETE Logic---------------------
@router.delete("/{student_id}")
def remove_student(student_id: int, current_user: dict = Depends(auth.get_current_user)):

    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete students"
        )
    
    try:
        result = services.delete_student_data(student_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))