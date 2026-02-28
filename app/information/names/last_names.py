def last_names(id: int):
    if id < 1 or id > 3:
        raise HTTPException(status_code=404, detail="Not Found")
    last_names = ["last_name1", "last_name2", "last_name3"]
    return last_names[id-1]