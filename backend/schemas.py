from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: str
    email: str

class LinkCreate(BaseModel):
    url: str
    title: str
    description: str = ""
    category: str = ""


class LinkResponse(BaseModel):
    id: int
    title: str
    url: str
    description: str
    category: str

    class Config:
        from_attributes = True

class URLRequest(BaseModel):
    url: str