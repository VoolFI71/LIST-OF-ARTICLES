from pydantic import BaseModel, UUID4


class User(BaseModel):
    nick: str
    password: str

class List(BaseModel):
    nick: str
    title: str
    description: str