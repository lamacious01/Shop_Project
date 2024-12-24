from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Dependency to get the database connection
def get_db():
    conn = sqlite3.connect("users.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    Product TEXT UNIQUE,
                    Cost INTEGER,
                    Stock INTEGER
                )""")
    return conn


# Pydantic model for request and response validation
class UserCreate(BaseModel):
    Product: str
    Cost: int
    Stock: int

class UserResponse(BaseModel):
    id: int
    Product: str
    Cost: int
    Stock: int

# Create a user
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db=Depends(get_db)):
    cursor = db.cursor()
    try:
        cursor.execute("""INSERT INTO users (Product, Cost, Stock) VALUES (?, ?, ?)""", 
                       (user.Product, user.Cost, user.Stock))
        db.commit()
        user_id = cursor.lastrowid
        return {"id": user_id, "Product": user.Product, "Cost": user.Cost, "Stock": user.Stock}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="It already exists")
    finally:
        db.close()

# Get a user by Product
@app.get("/users/{user_Product}", response_model=UserResponse)
def get_user(user_Product: str, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, Product, Cost, Stock FROM users WHERE id = ?", (user_Product,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    return {"id": user[0], "Product": user[1], "Cost": user[2], "Stock": user[3]}

# Get all users
@app.get("/users/", response_model=list[UserResponse])
def get_users(db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, Product, Cost, Stock FROM users")
    users = cursor.fetchall()
    return [{"id": user[0], "Product": user[1], "Cost": user[2], "Stock": user[3]} for user in users]

# Update a user
@app.put("/users/{user_Product}", response_model=UserResponse)
def update_user(user_Product: str, user: UserCreate, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("UPDATE users SET Cost = ?, Stock = ? WHERE id = ?",
                   (user.Cost, user.Stock, user_Product))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Not found")
    db.commit()
    return {"id": user.id, "Product": user_Product, "Cost": user.Cost, "Stock": user.Stock}

# Delete a user
@app.delete("/users/{user_Product}")
def delete_user(user_Product: str, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_Product,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Not found")
    db.commit()
    return {"Detail": "Product deleted successfully"}