from pydantic import BaseModel

class UserCreate(BaseModel):
    firstname: str
    lastname: str
    username: str
    password: str
    is_admin: bool = False

