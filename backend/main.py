from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, Base, get_db
import models
import schemas

from ai_service import summarize_link
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "VaultIQ API is running"}

@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    db_user = models.User(
        username=user.username,
        email=user.email,
        password=user.password
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

@app.post("/ai/summarize")
def ai_summarize(data: schemas.URLRequest):

    result = summarize_link(data.url)

    return {
        "result": result
    }

@app.post("/links")
def create_link(
    link: schemas.LinkCreate,
    db: Session = Depends(get_db)
):
    new_link = models.Link(
        title=link.title,
        url=link.url,
        description=link.description,
        category=link.category
    )

    db.add(new_link)
    db.commit()
    db.refresh(new_link)

    return new_link

@app.get("/links")
def get_links(db: Session = Depends(get_db)):
    return db.query(models.Link).all()

@app.delete("/links/{link_id}")
def delete_link(
    link_id: int,
    db: Session = Depends(get_db)
):
    link = db.query(models.Link).filter(
        models.Link.id == link_id
    ).first()

    if not link:
        return {"error": "Link not found"}

    db.delete(link)
    db.commit()

    return {"message": "Link deleted successfully"}

@app.post("/login")
def login_user(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if not db_user:
        return {"message": "User not found"}

    if db_user.password != user.password:
        return {"message": "Invalid password"}

    return {
        "message": "Login successful",
        "username": db_user.username
    }