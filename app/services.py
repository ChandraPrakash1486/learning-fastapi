import json 
from .config import STUDENTS_MARKS_FILE
from .schemas import SearchField, StudentCreate

def load_students_marks_data() -> dict:
    """Loads Students Marks Data from JSON file"""
    if not STUDENTS_MARKS_FILE.exists():
        return {}
    with open(STUDENTS_MARKS_FILE) as f:
        return json.load(f)


def filter_students_marks_data_by_field(all_students:  list, field: SearchField, value: str) -> list:
    """Filters the student's marks list by field and value"""
    if field == SearchField.FIRST_NAME:
        if len(value) < 2:
            raise ValueError("First name must be at least 2 characters long")
        return [student for student in all_students if student.get("first_name") == value]
    
    if field == SearchField.LAST_NAME:
        if len(value) < 2:
            raise ValueError("Last name must be at least 2 characters long")
        return [student for student in all_students if student.get("last_name") == value]
    
    if field == SearchField.ID:
        if not value.isdigit():
            raise ValueError("ID must be a number")
        return [student for student in all_students if student.get("id") == int(value)]
        
    return [] 

def create_student(student_data: StudentCreate) -> dict:
    # ""Takes validated pydantic data and saves it into the JSON file"""
    all_students = load_students_marks_data()
    
    existing_ids = [student.get("id") for student in all_students]
    next_id = max(existing_ids) + 1 if existing_ids else 1
    
    new_student_data = {
        "first_name": student_data.first_name,
        "last_name": student_data.last_name,
        "id": next_id,
        "marks": student_data.marks.model_dump()
    }

    all_students.append(new_student_data)

    with open(STUDENTS_MARKS_FILE, "w") as f:
        json.dump(all_students, f, indent=4)
    return new_student_data

    

    