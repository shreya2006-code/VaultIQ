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

@app.post("/links", response_model=schemas.LinkResponse)
def create_link(
    link: schemas.LinkCreate,
    db: Session = Depends(get_db)
):

    db_link = models.Link(
        title=link.title,
        url=link.url,
        description=link.description,
        category=link.category
    )

    db.add(db_link)
    db.commit()
    db.refresh(db_link)

    return db_link

@app.get("/links", response_model=list[schemas.LinkResponse])
def get_links(db: Session = Depends(get_db)):

    links = db.query(models.Link).all()

    return links

@app.delete("/links/{link_id}")
def delete_link(
    link_id: int,
    db: Session = Depends(get_db)
):

    link = db.query(models.Link).filter(
        models.Link.id == link_id
    ).first()

    db.delete(link)
    db.commit()

    return {"message": "Link deleted successfully"}