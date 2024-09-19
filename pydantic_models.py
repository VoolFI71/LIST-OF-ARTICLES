from pydantic import BaseModel, UUID4

class Message(BaseModel):
    message: str

class User(BaseModel):
    nick: str
    password: str
    name: str | None = None
    email: str | None = None
    age: int | None = None
    city: str | None = None
    
class Reg_User(User):
    password2: str

class List(BaseModel):
    title: str
    description: str