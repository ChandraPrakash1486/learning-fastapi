def full_names(id: int):
    if id < 1 or id > 3:
        raise HTTPException(status_code=404, detail="Not Found")
    full_names = ["first_name1 last_name1", "first_name2 last_name2", "first_name3 last_name3"]
    return full_names[id-1]