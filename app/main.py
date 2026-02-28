from fastapi import FastAPI
from information.names.first_names import first_names
from information.names.last_names import last_names
from information.names.full_names import full_names



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