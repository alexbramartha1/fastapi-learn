from pydantic import BaseModel

class UserData(BaseModel):
    _id: str
    nama: str 
    email: str
    foto_profile: str = None
    password: str

class UserInDB(UserData):
    _id: str
    nama: str 
    email: str
    foto_profile: str = None
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str = None