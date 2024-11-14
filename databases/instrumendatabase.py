from models.instrumen import *
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
import os

uri = "mongodb://alexbramartha14:WCknO6oCCiM8r3qC@tagamelanbaliakhir-shard-00-00.zx7dr.mongodb.net:27017,tagamelanbaliakhir-shard-00-01.zx7dr.mongodb.net:27017,tagamelanbaliakhir-shard-00-02.zx7dr.mongodb.net:27017/?ssl=true&replicaSet=atlas-qfuxr3-shard-0&authSource=admin&retryWrites=true&w=majority&appName=TAGamelanBaliAkhir"
client = AsyncIOMotorClient(uri)

database = client["tugas-akhir-data"]

collection = database["instrumen-gamelan"]

async def fetch_byname_instrumen(name: str):
    instrument = []

    cursor = collection.find({"nama_instrument": {"$regex": f"(?i){name}"}})
    
    async for document in cursor:
        instrumen_data = {
            "_id": str(document["_id"]),
            "nama_instrument": document["nama_instrument"],
            "description": document["description"],
            "trid_image": document["trid_image"],
            "fungsi": document["fungsi"],
            "image_instrumen": document["image_instrumen"],
            "status": document["status"],
            "bahan": document["bahan"]
        }

        instrument.append(instrumen_data)
    
    return instrument
                                                  
async def fetch_all_instrumen():
    instrumen = []

    cursor = collection.find({})

    async for document in cursor:
        instrumen_data = {
            "_id": str(document["_id"]),
            "nama_instrument": document["nama_instrument"],
            "description": document["description"],
            "trid_image": document["trid_image"],
            "fungsi": document["fungsi"],
            "image_instrumen": document["image_instrumen"],
            "status": document["status"],
            "bahan": document["bahan"]
        }

        instrumen.append(instrumen_data)
    
    return instrumen

async def create_instrumen_data(nama: str, desc: str, tridi: str, fungsi: str, image_instrumen: str, bahan: List[str]):
    data: InstrumenData

    for bahanData in bahan:
        if bahanData:
            print(bahanData)

    data = {
        "nama_instrument": nama,
        "description": desc,
        "trid_image": tridi,
        "fungsi": fungsi,
        "image_instrumen": image_instrumen,
        "status": "unapproved",
        "bahan": bahan
    }

    document = await collection.insert_one(data)

    return {"_id": str(document.inserted_id), "nama_instrument": nama, "message": "Data created successfully"}

async def update_instrumen_data(id: str, nama: str, desc: str, fungsi: str, tridi: str, image_instrumen: str, bahan: List[str]):
    objectId = ObjectId(id)
    
    data_updated = {}
    
    if bahan:
        bahan = [data for data in bahan if data and data != "string"]

        data_updated["bahan"] = bahan
    
    if not bahan:
        bahan = None

    if nama:
        data_updated["nama_instrument"] = nama

    if desc:
        data_updated["description"] = desc

    if fungsi:
        data_updated["fungsi"] = fungsi

    if tridi:
        data_updated["trid_image"] = tridi

    if image_instrumen:
        data_updated["image_instrumen"] = image_instrumen

    await collection.update_one(
        {"_id": objectId},
        {"$set": data_updated},
    )

    return {"message": "Data updated successfully", "Updated_data": data_updated}

async def fetch_one_instrumen(id: str):
    object_id = ObjectId(id)
    document = await collection.find_one({"_id": object_id})
    return document

async def fetch_tridi_instrumen(id: str):
    object_id = ObjectId(id)
    document = await collection.find_one({"_id": object_id})
    tridi_path = document.get("trid_image")
    return tridi_path

async def fetch_image_instrumen(id: str):
    object_id = ObjectId(id)
    document = await collection.find_one({"_id": object_id})
    image_path = document.get("image_instrumen")
    return image_path

async def delete_instrument_bali(id: str):
    object_id = ObjectId(id)

    instrumen_image = []
    instrumen_tridi = []

    cursor = collection.find({"_id": object_id})

    async for document in cursor:
        instrumen_data_image = document["image_instrumen"]

        instrumen_data_tridi = document["trid_image"]

        instrumen_tridi.append(instrumen_data_tridi)
        instrumen_image.append(instrumen_data_image)

    for path_todelete_tridi in instrumen_tridi:
        if os.path.exists(path_todelete_tridi):
            os.remove(path_todelete_tridi)
            print(f"The file {path_todelete_tridi} has been deleted.")
        else:
            print(f"The file {path_todelete_tridi} does not exist.")

    for path_todelete_image in instrumen_image:
        if os.path.exists(path_todelete_image):
            os.remove(path_todelete_image)
            print(f"The file {path_todelete_image} has been deleted.")
        else:
            print(f"The file {path_todelete_image} does not exist.")

    await collection.delete_one({"_id": object_id})

    return True

async def approval_instrunmen_data(id: str, status: str):
    object_id = ObjectId(id)

    if status == "approved":
        await collection.update_one({"_id": object_id}, {"$set": {"status": status}})

        return f"Data Instrumen Gamelan Bali {status}"
    
    if status == "unapproved":
        await collection.update_one({"_id": object_id}, {"$set": {"status": status}})

        return f"Data Instrumen Gamelan Bali {status}"
