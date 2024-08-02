from pydantic import BaseModel, UUID4


class User(BaseModel):
    nick: str
    password: str

class Reg_User(User):
    password2: str
class List(BaseModel):
    title: str
    description: str