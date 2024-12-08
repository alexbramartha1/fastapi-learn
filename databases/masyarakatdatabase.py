from models.masyarakat import *
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
import re
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
import time
from datetime import datetime

uri = "mongodb://alexbramartha14:WCknO6oCCiM8r3qC@tagamelanbaliakhir-shard-00-00.zx7dr.mongodb.net:27017,tagamelanbaliakhir-shard-00-01.zx7dr.mongodb.net:27017,tagamelanbaliakhir-shard-00-02.zx7dr.mongodb.net:27017/?ssl=true&replicaSet=atlas-qfuxr3-shard-0&authSource=admin&retryWrites=true&w=majority&appName=TAGamelanBaliAkhir"
client = AsyncIOMotorClient(uri)

database = client["tugas-akhir-data"]

collection = database["pengguna-masyarakat"]

async def get_user(email: str):
    local_part, domain = email.split('@')

    user_dict = await collection.find_one({
        "email": {
            "$regex": f"^{local_part}@{domain}$", 
            "$options": "i"
        }
    })

    print(user_dict)
    
    if user_dict:
        ts = user_dict["createdAt"]
        dt = datetime.fromtimestamp(ts)
        tanggal = dt.date()
        waktu = dt.time()

        updateTs = user_dict["updatedAt"]
        updateDt = datetime.fromtimestamp(updateTs)
        updateTanggal = updateDt.date()
        updateWaktu = updateDt.time()

        user_dict["_id"] = str(user_dict["_id"])
        print(user_dict)
        user = UserInDB(
            _id=user_dict["_id"],
            nama=user_dict["nama"],
            email=user_dict["email"],
            foto_profile=user_dict["foto_profile"],
            password=user_dict["password"],
            test=user_dict["_id"],
            status=user_dict["status"],
            createdAtTime=str(waktu),
            createdAtDate=str(tanggal),
            updatedAtTime=str(updateWaktu),
            updatedAtDate=str(updateTanggal),
            role=user_dict["role"]
        )

        return user

    return None

async def fetch_one_user(id: str):
    object_id = ObjectId(id)
    
    user_data_full = []

    document = collection.find({"_id": object_id})

    async for user in document:
        ts = user["createdAt"]
        dt = datetime.fromtimestamp(ts)
        tanggal = dt.date()
        waktu = dt.time()

        updateTs = user["updatedAt"]
        updateDt = datetime.fromtimestamp(updateTs)
        updateTanggal = updateDt.date()
        updateWaktu = updateDt.time()
        
        user_data = {
            "_id": str(user["_id"]),
            "nama": user["nama"],
            "email": user["email"],
            "foto_profile": user["foto_profile"],
            "password": user["password"],
            "createdAt": dt,
            "createdDate": tanggal,
            "createdTime": waktu,
            "updatedAt": updateDt,
            "updatedDate": updateTanggal,
            "updateTime": updateWaktu,
            "status": user["status"],
            "role": user["role"]
        }

        user_data_full.append(user_data)

    return {"data_user": user_data_full}

async def fetch_user_specific(email: str):
    local_part, domain = email.split('@')

    document = await collection.find_one({"email": {"$regex": f"^{local_part}@{domain}$", 
            "$options": "i"
            }})
    
    return {"data_user": document}

async def fetch_all_user_with_name(name: str):
    user = []
    cursor = collection.find({"nama": {"$regex": f"(?i){name}"}})

    async for document in cursor:
        ts = document["createdAt"]
        dt = datetime.fromtimestamp(ts)
        tanggal = dt.date()
        waktu = dt.time()

        updateTs = document["updatedAt"]
        updateDt = datetime.fromtimestamp(updateTs)
        updateTanggal = updateDt.date()
        updateWaktu = updateDt.time()
        
        user_data = {
            "_id": str(document["_id"]),
            "nama": document["nama"],
            "email": document["email"],
            "foto_profile": document["foto_profile"],
            "password": document["password"],
            "createdAt": dt,
            "createdDate": tanggal,
            "createdTime": waktu,
            "updatedAt": updateDt,
            "updatedDate": updateTanggal,
            "updateTime": updateWaktu,
            "status": document["status"],
            "role": document["role"]
        }
        user.append(user_data)
    
    return {"data_user": user}

async def fetch_all_user():
    user = []
    cursor = collection.find({})

    async for document in cursor:
        ts = document["createdAt"]
        dt = datetime.fromtimestamp(ts)
        tanggal = dt.date()
        waktu = dt.time()

        updateTs = document["updatedAt"]
        updateDt = datetime.fromtimestamp(updateTs)
        updateTanggal = updateDt.date()
        updateWaktu = updateDt.time()

        user_data = {
            "_id": str(document["_id"]),
            "nama": document["nama"],
            "email": document["email"],
            "foto_profile": document["foto_profile"],
            "password": document["password"],
            "createdAt": dt,
            "createdDate": tanggal,
            "createdTime": waktu,
            "updatedAt": updateDt,
            "updatedDate": updateTanggal,
            "updateTime": updateWaktu,
            "status": document["status"],
            "role": document["role"]
        }

        user.append(user_data)
    
    return {"data_user": user}

async def create_user_data(nama: str, email: str, password: str):
    document: UserData
    
    timestamps = time.time()

    document = {
        "nama": nama,
        "email": email,
        "foto_profile": "none",
        "password": password,
        "createdAt": timestamps,
        "updatedAt": timestamps,
        "status": "approved",
        "role": "masyarakat"
    }

    result = await collection.insert_one(document)
    
    return {"_id": str(result.inserted_id), "nama": nama, "message": "Data created successfully"}

async def update_user_data(id: str, email: str, nama: str):
    object_id = ObjectId(id)

    update_data = {}

    timestamps = time.time()
    
    if nama:
        update_data["nama"] = nama

    if email:
        update_data["email"] = email 

    if update_data:
        update_data["updatedAt"] = timestamps

    await collection.update_one(
        {"_id": object_id},
        {"$set": update_data},
    )

    document = await collection.find_one({"_id": object_id})
    
    return document

async def update_user_photo(id: str, foto: str):
    object_id = ObjectId(id)
    
    updated_data = {}
    timestamps = time.time()

    if foto:
        updated_data["foto_profile"] = foto

    if updated_data:
        updated_data["updatedAt"] = timestamps

    await collection.update_one({"_id": object_id}, {"$set": updated_data})

    document = await collection.find_one({"_id": object_id})
    
    return document

async def delete_user_data(id: str):
    object_id = ObjectId(id)
    
    foto_profile = []

    cursor = collection.find({"_id": object_id})

    async for document in cursor:
        foto_profile_data = document["foto_profile"]
    
        foto_profile.append(foto_profile_data)

    for path_todelete_foto in foto_profile:
        public_id = extract_public_id(path_todelete_foto)

        cloudinary.uploader.destroy(public_id)
    
    await collection.delete_one({"_id": object_id})

    return True

def extract_public_id(secure_url):
    pattern = r"/upload/(?:v\d+/)?(.+)\.\w+$"
    match = re.search(pattern, secure_url)
    if match:
        return match.group(1)
    else:
        return None
# async def delete_user_data(name):
#     await collection.delete_one({"nama": {"$regex": f"(?i){name}"}})
#     return True
