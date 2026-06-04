from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from backend.database import engine, Base, get_db
from backend import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "VaultIQ API is running"}

@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    db_user = models.User(
        username=user.username,
        email=user.email
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):

    users = db.query(models.User).all()

    return users

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == user_id).first()

    return user

@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    updated_user: schemas.UserUpdate,
    db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    user.username = updated_user.username
    user.email = updated_user.email

    db.commit()
    db.refresh(user)

    return user

@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}