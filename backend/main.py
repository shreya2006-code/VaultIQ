from fastapi import FastAPI

from backend.database import engine, Base
from backend import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "VaultIQ API is running"}