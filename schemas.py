from pydantic import BaseModel

class  UserCreate(BaseModel):
    username : str
    password: str
    email :str


class UserLogin(BaseModel):
    username : str
    password: str
    
class Token(BaseModel):
    access_token : str
    token_type : str        