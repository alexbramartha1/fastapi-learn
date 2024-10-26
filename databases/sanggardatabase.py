from models.sanggarbali import *
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId

uri = "mongodb://alexbramartha14:WCknO6oCCiM8r3qC@tagamelanbaliakhir-shard-00-00.zx7dr.mongodb.net:27017,tagamelanbaliakhir-shard-00-01.zx7dr.mongodb.net:27017,tagamelanbaliakhir-shard-00-02.zx7dr.mongodb.net:27017/?ssl=true&replicaSet=atlas-qfuxr3-shard-0&authSource=admin&retryWrites=true&w=majority&appName=TAGamelanBaliAkhir"
client = AsyncIOMotorClient(uri)

database = client["tugas-akhir-data"]

collection = database["sanggar-gamelan"]

async def fetch_all_sanggar():
    sanggar = []

    cursor = collection.find({})

    async for document in cursor:
        sanggar_data = {
            "_id": str(document["_id"]),
            "image": document["image"],
            "nama_sanggar": document["nama_sanggar"],
            "alamat": document["alamat"],
            "no_telepon": document["no_telepon"],
            "latitude": document["latitude"],
            "longitude": document["longitude"],
            "id_creator": document["id_creator"]
        }
        
        sanggar.append(sanggar_data)
    
    return sanggar

