from pydantic import BaseModel, Field

class UserData(BaseModel):
    _id: str
    nama: str 
    email: str
    foto_profile: str = None
    password: str
    createdAt: str
    updatedAt: str
    status: str
    role: str
    support_document: str = None

class UserInDB(BaseModel):
    _id: str 
    nama: str 
    email: str
    foto_profile: str = None
    password: str
    test: str
    createdAtTime: str
    createdAtDate: str
    updatedAtTime: str
    updatedAtDate: str
    status: str
    role: str
    support_document: str = None

class Token(BaseModel):
    access_token: str
    user_id: str
    nama: str 
    email: str
    foto_profile: str = None
    createdAtTime: str
    createdAtDate: str
    updatedAtTime: str
    updatedAtDate: str
    status: str
    role: str
    support_document: str = None
    token_type: str

class TokenData(BaseModel):
    email: str = None