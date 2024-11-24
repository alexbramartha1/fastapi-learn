from models.instrumen import *
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
import re
import time
from datetime import datetime
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

uri = "mongodb://alexbramartha14:WCknO6oCCiM8r3qC@tagamelanbaliakhir-shard-00-00.zx7dr.mongodb.net:27017,tagamelanbaliakhir-shard-00-01.zx7dr.mongodb.net:27017,tagamelanbaliakhir-shard-00-02.zx7dr.mongodb.net:27017/?ssl=true&replicaSet=atlas-qfuxr3-shard-0&authSource=admin&retryWrites=true&w=majority&appName=TAGamelanBaliAkhir"
client = AsyncIOMotorClient(uri)

database = client["tugas-akhir-data"]

collection = database["instrumen-gamelan"]

async def fetch_byname_instrumen(name: str):
    instrument = []

    cursor = collection.find({"nama_instrument": {"$regex": f"(?i){name}"}})
    
    async for document in cursor:
        ts = document["createdAt"]
        dt = datetime.fromtimestamp(ts)
        tanggal = dt.date()
        waktu = dt.time()

        updateTs = document["updatedAt"]
        updateDt = datetime.fromtimestamp(updateTs)
        updateTanggal = updateDt.date()
        updateWaktu = updateDt.time()

        instrumen_data = {
            "_id": str(document["_id"]),
            "nama_instrument": document["nama_instrument"],
            "description": document["description"],
            "trid_image": document["trid_image"],
            "fungsi": document["fungsi"],
            "image_instrumen": document["image_instrumen"],
            "status": document["status"],
            "bahan": document["bahan"],
            "createdAt": dt,
            "createdDate": tanggal,
            "createdTime": waktu,
            "updatedAt": updateDt,
            "updatedDate": updateTanggal,
            "updateTime": updateWaktu
        }

        instrument.append(instrumen_data)
    
    return {
        "instrument_data": instrument
    }
                                                  
async def fetch_all_instrumen():
    instrumen = []

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

        instrumen_data = {
            "_id": str(document["_id"]),
            "nama_instrument": document["nama_instrument"],
            "description": document["description"],
            "trid_image": document["trid_image"],
            "fungsi": document["fungsi"],
            "image_instrumen": document["image_instrumen"],
            "status": document["status"],
            "bahan": document["bahan"],
            "createdAt": dt,
            "createdDate": tanggal,
            "createdTime": waktu,
            "updatedAt": updateDt,
            "updatedDate": updateTanggal,
            "updateTime": updateWaktu
        }

        instrumen.append(instrumen_data)
    
    return {
        "instrument_data": instrumen
    }

async def create_instrumen_data(nama: str, desc: str, tridi: str, fungsi: str, image_instrumen: str, bahan: List[str]):
    data: InstrumenData

    for bahanData in bahan:
        if bahanData:
            print(bahanData)

    timestamps = time.time()

    data = {
        "nama_instrument": nama,
        "description": desc,
        "trid_image": tridi,
        "fungsi": fungsi,
        "image_instrumen": image_instrumen,
        "status": "unapproved",
        "bahan": bahan,
        "createdAt": timestamps,
        "updatedAt": timestamps
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

    timestamps = time.time()
    
    if data_updated:
        data_updated["updatedAt"] = timestamps

    await collection.update_one(
        {"_id": objectId},
        {"$set": data_updated},
    )

    return {"message": "Data updated successfully", "Updated_data": data_updated}

async def fetch_one_instrumen(id: str):
    object_id = ObjectId(id) 
    instrument = []

    document = await collection.find_one({"_id": object_id})
    
    ts = document["createdAt"]
    dt = datetime.fromtimestamp(ts)
    tanggal = dt.date()
    waktu = dt.time()

    updateTs = document["updatedAt"]
    updateDt = datetime.fromtimestamp(updateTs)
    updateTanggal = updateDt.date()
    updateWaktu = updateDt.time()

    instrumen_data = {
        "_id": str(document["_id"]),
        "nama_instrument": document["nama_instrument"],
        "description": document["description"],
        "trid_image": document["trid_image"],
        "fungsi": document["fungsi"],
        "image_instrumen": document["image_instrumen"],
        "status": document["status"],
        "bahan": document["bahan"],
        "createdAt": dt,
        "createdDate": tanggal,
        "createdTime": waktu,
        "updatedAt": updateDt,
        "updatedDate": updateTanggal,
        "updateTime": updateWaktu
    }

    instrument.append(instrumen_data)
    
    return {
        "instrument_data": instrument
    }

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
        public_id = extract_public_id(path_todelete_tridi)

        cloudinary.uploader.destroy(public_id)

    for path_todelete_image in instrumen_image:
        public_id = extract_public_id(path_todelete_image)

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

async def approval_instrunmen_data(id: str, status: str):
    object_id = ObjectId(id)

    timestamps = time.time()
    
    if status == "approved":
        await collection.update_one({"_id": object_id}, {"$set": {"status": status, "updatedAt": timestamps}})

        return f"Data Instrumen Gamelan Bali {status}"
    
    if status == "unapproved":
        await collection.update_one({"_id": object_id}, {"$set": {"status": status, "updatedAt": timestamps}})

        return f"Data Instrumen Gamelan Bali {status}"
