import json 
from .config import STUDENTS_MARKS_FILE
from .schemas import SearchField, StudentCreate, StudentCreatePatch

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


def update_student_full_data(student_id: int, student_data: StudentCreate) -> dict:
    all_students = load_students_marks_data()

    for i, student in enumerate(all_students):
        if student.get("id") == student_id:
            updated_studet_data = {
                "first_name": student_data.first_name,
                "last_name": student_data.last_name,
                "id": student_data.id,
                "marks": student_data.marks.model_dump()
            }
            all_students[i] = updated_studet_data
            with open(STUDENTS_MARKS_FILE, "w") as f:
                json.dump(all_students, f, indent=4)
            return updated_studet_data
    raise HTTPException(status_code=404, detail="Student not found")


def update_student_partial_data(student_id: int, patch_data: StudentCreatePatch) -> dict:
    all_students = load_students_marks_data() #this loads the data from the JSON file as a list of dictionaries 

    for i, student in enumerate(all_students): #i is the index of the student in the list, and student is the student dictionary
        if student.get("id") == student_id:
            updated_data = patch_data.model_dump(exclude_unset=True) #exclude_unset=True excludes any fields that are not set in the request

            if "first_name" in updated_data:
                student["first_name"] = updated_data["first_name"]

            if "last_name" in updated_data:
                student["last_name"] = updated_data["last_name"]

            if "marks" in updated_data:
                for subject, score in updated_data["marks"].items():
                    student["marks"][subject] = score

            all_students[i] = student #updates the student dictionary with the updated data


            with open(STUDENTS_MARKS_FILE, "w") as f:
                json.dump(all_students, f, indent=4)
            return student

    raise HTTPException(status_code=404, detail="Student not found")

    

    