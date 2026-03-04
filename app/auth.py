import json
from fastapi import Depends, HTTPException, status
from .config import USERS_FILE

def load_users() -> dict:
    with open(USERS_FILE, "r") as f:
        return json.load(f)

#--------Authorization Logic-------
def get_current_user(token: str) -> dict:
    users = load_users()
    username = token.replace("-secret-token", "")
    
    if username not in users:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    
    user_profile = users[username]
    user_profile["username"] = username 
    return user_profile