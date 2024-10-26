from models.masyarakat import *
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId

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

    if user_dict:
        user_dict["_id"] = str(user_dict["_id"])
        return UserInDB(**user_dict)

    return None

async def fetch_one_user(id):
    object_id = ObjectId(id)
    document = await collection.find_one({"_id": object_id})
    return document

async def fetch_user_specific(email):
    local_part, domain = email.split('@')

    document = await collection.find_one({"email": {"$regex": f"^{local_part}@{domain}$", 
            "$options": "i"
            }})
    
    return document

async def fetch_all_user_with_name(name):
    user = []
    cursor = collection.find({"nama": {"$regex": f"(?i){name}"}})

    async for document in cursor:
        user_data = {
            "_id": str(document["_id"]),
            "nama": document["nama"],
            "email": document["email"],
            "foto_profile": document["foto_profile"],
            "password": document["password"] 
        }
        user.append(user_data)
    
    return user

async def fetch_all_user():
    user = []
    cursor = collection.find({})

    async for document in cursor:
        user_data = {
            "_id": str(document["_id"]),
            "nama": document["nama"],
            "email": document["email"],
            "foto_profile": document["foto_profile"],
            "password": document["password"] 
        }

        user.append(user_data)
    
    return user

async def create_user_data(nama, email, password):
    document: UserData

    document = {
        "nama": nama,
        "email": email,
        "foto_profile": "none",
        "password": password,
    }

    result = await collection.insert_one(document)
    
    return {"_id": str(result.inserted_id), "nama": nama, "message": "Data created successfully"}

async def update_user_data(id, email, nama):
    object_id = ObjectId(id)
    await collection.update_one(
        {"_id": object_id},
        {"$set":{"email":email, "nama":nama}},
    )

    document = await collection.find_one({"_id": object_id})
    return document

async def update_user_photo(id, foto):
    object_id = ObjectId(id)
    await collection.update_one({"_id": object_id}, {"$set":{"foto_profile": foto}})
    document = await collection.find_one({"_id": object_id})
    return document

async def delete_user_data(id):
    object_id = ObjectId(id)
    await collection.delete_one({"_id": object_id})
    return True

# async def delete_user_data(name):
#     await collection.delete_one({"nama": {"$regex": f"(?i){name}"}})
#     return True
