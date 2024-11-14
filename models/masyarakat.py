from pydantic import BaseModel, Field

class UserData(BaseModel):
    _id: str
    nama: str 
    email: str
    foto_profile: str = None
    password: str

class UserInDB(BaseModel):
    _id: str 
    nama: str 
    email: str
    foto_profile: str = None
    password: str
    test: str

class Token(BaseModel):
    access_token: str
    user_id: str
    nama: str 
    email: str
    foto_profile: str = None
    token_type: str

class TokenData(BaseModel):
    email: str = None