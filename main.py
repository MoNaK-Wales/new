from fastapi import FastAPI
from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: str

users = [
    User(id=1, username="johndoe", email="john@example.com"),
    User(id=2, username="janedoe", email="jane@example.com"),
    User(id=3, username="alice", email="alice@example.com"),
]
    
app = FastAPI()

@app.get("/users")
def get_users():
    return users

@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user

@app.post("/create_user")
def create_user(user: User):
    users.append(user)
    return user


if __name__ == "__main__":
    import os
    os.system("python -m uvicorn main:app --reload")