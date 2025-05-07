from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3


db = "users.db"
db_connection = sqlite3.connect(db)
cursor = db_connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL
)
""")
db_connection.commit()
db_connection.close()

class User(BaseModel):
    id: int
    username: str
    email: str
    
app = FastAPI()

@app.get("/users")
def get_users():
    con = sqlite3.connect(db)
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    con.close()
    return [User(id=row[0], username=row[1], email=row[2]) for row in rows]

@app.get("/users/{user_id}")
def get_user(user_id: int):
    con = sqlite3.connect(db)
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    con.close()
    if row:
        return User(id=row[0], username=row[1], email=row[2])

@app.post("/create_user")
def create_user(user: User):
    con = sqlite3.connect(db)
    cursor = con.cursor()
    cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (user.username, user.email))
    con.commit()
    con.close()
    return user


if __name__ == "__main__":
    import os
    os.system("python -m uvicorn main:app --reload")