from fastapi import APIRouter, Query, Path, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
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



@router.post("/login")
def login_for_access_token(user_data: OAuth2PasswordRequestForm = Depends()):
    users = auth.load_users()
    
    #Verify if User exists
    if user_data.username not in users:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    #Verify if Password is correct
    if not auth.verify_password(user_data.password, users[user_data.username]["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    
    
    #Create the JWT token
    access_token = auth.create_access_token(data={"sub": user_data.username})
    
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

#Create Decure DELETE
@router.delete("/{student_id}")
def remove_student(student_id: int = Path(..., ge=1), current_user: dict = Depends(auth.get_current_user)):
    #check role
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    try:
        result = services.delete_student_data(student_id)
        return result

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))