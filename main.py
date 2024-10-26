from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from models.masyarakat import *
import os
from datetime import timedelta, datetime, timezone
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
import re
from typing import Annotated
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, PyJWTError

from databases.masyarakatdatabase import (
    fetch_one_user, 
    fetch_all_user,
    create_user_data,
    update_user_data,
    delete_user_data,
    update_user_photo,
    fetch_all_user_with_name,
    fetch_user_specific,
    get_user,
)

from databases.sanggardatabase import (
    fetch_all_sanggar,
)

SECRET_KEY = "letsmekillyou"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def authenticate_user(email: str, password: str):
    user = await get_user(email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)    
        user = await get_user(email=token_data.email)
        if user is None:
            raise credentials_exception
    except ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired, please login again!")
    except InvalidTokenError:
        raise HTTPException(status_code=400, detail="Token Invalid!")
    except JWTError:
        raise HTTPException(status_code=400, detail="Token Invalid!")
    except AttributeError:
        raise HTTPException(status_code=400, detail="Token has expired, please login again!")
    
    return user

async def get_current_active_user(
    current_user: Annotated[UserInDB, Depends(get_current_user)],
):
    if not current_user.email:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={
            "nama": str(user.nama),
            "sub": str(user.email),
            "foto_profile": str(user.foto_profile),
            }, 
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")

@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}

@app.get("/api/userdata")
async def get_all_users(current_user: UserInDB = Depends(get_current_user)):
    if current_user:
        response = await fetch_all_user()
        if response:
            return response
        raise HTTPException(404, "Empty Users Data")

@app.get("/api/userdata/getallbyname/{name}")
async def get_all_user_by_name(name: str):
    response = await fetch_all_user_with_name(name)
    if response:
        return response
    raise HTTPException(404, f"There is no user with this name {name}")

@app.get("/api/userdata/getspecific/{email}")
async def get_specific_by_email(email: str):
    valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

    if valid:
        response = await fetch_user_specific(email)
        if not response:
            return response
        raise HTTPException(404, f"Email already exists")
    raise HTTPException(404, f"Email not Valid!")

@app.get("/api/userdata/{id}", response_model=UserData)
async def get_user_by_id(id: str):
    response = await fetch_one_user(id)
    if response:
        return response
    raise HTTPException(404, f"There is no user with this name {id}")

@app.post("/api/userdata")
async def create_data_user(nama: str, email: str, password: str):
    await get_specific_by_email(email)

    password_hashed = get_password_hash(password)

    response = await create_user_data(nama, email, password_hashed)
    if response:
        return response
    raise HTTPException(400, "Something went wrong!")

@app.put("/api/userdata/updateprofile/{id}", response_model=UserData)
async def update_data_user(id: str, email: str, nama: str):
    await get_specific_by_email(email)

    response = await update_user_data(id, email, nama)
    if response:
        return response
    raise HTTPException(404, f"There is no user with this name {id}")

@app.post("/api/files/")
async def create_file(id: str, files: list[UploadFile]):
    try: 
        saved_files = []
        file_paths = []

        for file in files:
            file_path = os.path.join(r"C:\Users\Alex Bramartha\Downloads\fastapi-learn\files\images", file.filename)
            
            with open(file_path, "wb") as f:
                f.write(file.file.read())
            
            saved_files.append(file.filename)
            file_paths.append(str(file_path))

        image_path = file_paths[0]
        await update_photo_user(id, image_path)

        return {"message": "Files saved successfully", "files": saved_files}
        
    except Exception as e:
        return {"message": f"Error occurred: {str(e)}"}

@app.put("/api/userdata/{id}", response_model=UserData)
async def update_photo_user(id: str, foto: str):
    response = await update_user_photo(id, foto)
    if response:
        return response
    raise HTTPException(404, f"There is no user with this name {id}")

@app.delete("/api/userdata/{id}")
async def delete_data_user(id: str):
    response = await delete_user_data(id)
    if response:
        return "Successfully deleted user!"
    raise HTTPException(404, f"There is no user with this name {id}")

@app.get("/api/sanggardata/fetchall")
async def fetch_sanggar_all_data(current_user: UserInDB = Depends(get_current_user)):
    if current_user:
        response = await fetch_all_sanggar()
        if response:
            return response
        raise HTTPException(404, "Empty Sanggar Data")
    