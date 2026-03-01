import json 
from .config import STUDENTS_MARKS_FILE
from .schemas import SearchField

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

    