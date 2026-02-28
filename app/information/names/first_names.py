from fastapi import HTTPException

def first_names(id: int):
    if id < 1 or id > 3:
        raise HTTPException(status_code=404, detail="Not Found")
    first_names = ["first_name1", "first_name2", "first_name3"]
    return first_names[id-1]