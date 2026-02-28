from fastapi import FastAPI, Query
from information.names.first_names import first_names
from information.names.last_names import last_names
from information.names.full_names import full_names
from information.full_info import full_info


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello Student"}

@app.get("/students/{id}")
def get_full_names(id: int):
    return full_names(id)

@app.get("/students/first_names/{id}")
def get_first_name(id: int):
    return first_names(id)
    

@app.get("/students/last_names/{id}")
def get_last_names(id: int):
    return last_names(id)


full_info = full_info()
@app.get("/students")
def get_full_info_by_name(id: int = Query(None), first_name: str = Query(None), last_name: str = Query(None), description="Search by the name, id or last name of the student"):
    matches = []
    for student, info in full_info.items():
        if id is not None and info["id"] != id:
            continue
        if first_name is not None and first_name.strip().lower() not in info["first_name"].lower():
            continue
        if last_name is not None and last_name.strip().lower() not in info["last_name"].lower():
            continue
        matches.append(info)
    if not matches:
        return {"error": "No student found"}
    return matches
        

