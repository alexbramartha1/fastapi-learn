from models.sanggarbali import *
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
import os

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
            "alamat_lengkap": document["alamat_lengkap"],
            "no_telepon": document["no_telepon"],
            "nama_jalan": document["nama_jalan"],
            "desa": document["desa"],
            "kecamatan": document["kecamatan"],
            "kabupaten": document["kabupaten"],
            "provinsi": document["provinsi"],
            "kode_pos": document["kode_pos"],
            "id_creator": document["id_creator"]
        }

        sanggar.append(sanggar_data)
    
    return sanggar

async def fetch_one_sanggar(id: str):
    object_id = ObjectId(id)
    document = await collection.find_one({"_id": object_id})
    image_path = document.get("image")
    return image_path

async def fetch_sanggar_specific(name: str):
    sanggar = []
    cursor = collection.find({"nama_sanggar": {"$regex": f"(?i){name}"}})
    
    async for document in cursor:
        sanggar_data = {
            "_id": str(document["_id"]),
            "image": document["image"],
            "nama_sanggar": document["nama_sanggar"],
            "alamat_lengkap": document["alamat_lengkap"],
            "no_telepon": document["no_telepon"],
            "nama_jalan": document["nama_jalan"],
            "desa": document["desa"],
            "kecamatan": document["kecamatan"],
            "kabupaten": document["kabupaten"],
            "provinsi": document["provinsi"],
            "kode_pos": document["kode_pos"],
            "id_creator": document["id_creator"]
        }

        sanggar.append(sanggar_data)
    
    return sanggar


async def fetch_sanggar_specific_by_id_creator(id: str):
    sanggar = []
    cursor = collection.find({"id_creator": id})
    
    async for document in cursor:
        sanggar_data = {
            "_id": str(document["_id"]),
            "image": document["image"],
            "nama_sanggar": document["nama_sanggar"],
            "alamat_lengkap": document["alamat_lengkap"],
            "no_telepon": document["no_telepon"],
            "nama_jalan": document["nama_jalan"],
            "desa": document["desa"],
            "kecamatan": document["kecamatan"],
            "kabupaten": document["kabupaten"],
            "provinsi": document["provinsi"],
            "kode_pos": document["kode_pos"],
            "id_creator": document["id_creator"]
        }
        
        sanggar.append(sanggar_data)
    
async def create_sanggar_data(
    image: str, 
    nama: str, 
    alamat: str, 
    no_telepon: str, 
    nama_jalan: str, 
    desa: str, 
    kecamatan: str,
    kabupaten: str,
    provinsi: str,
    kode_pos: str,
    id_creator: str
    ):
    
    data_sanggar: SanggarData
    
    data_sanggar = {
        "image": image,
        "nama_sanggar": nama,
        "alamat_lengkap": alamat,
        "no_telepon": no_telepon,
        "nama_jalan": nama_jalan,
        "desa": desa,
        "kecamatan": kecamatan,
        "kabupaten": kabupaten,
        "provinsi": provinsi,
        "kode_pos": kode_pos,
        "id_creator": id_creator
    }

    result = await collection.insert_one(data_sanggar)

    return {"_id": str(result.inserted_id), "nama_sanggar": nama, "message": "Data created successfully"}

async def update_sanggar_data(
    id: str, 
    nama: str, 
    alamat: str, 
    no_telepon: str,
    nama_jalan: str, 
    desa: str, 
    kecamatan: str,
    kabupaten: str,
    provinsi: str,
    kode_pos: str,
    ):
    
    object_id = ObjectId(id)

    update_data = {}
    
    if nama:
        update_data["nama_sanggar"] = nama
    
    if alamat:
        update_data["alamat_lengkap"] = alamat
    
    if no_telepon:
        update_data["no_telepon"] = no_telepon
    
    if nama_jalan:
        update_data["nama_jalan"] = nama_jalan

    if desa:
        update_data["desa"] = desa

    if kecamatan:
        update_data["kecamatan"] = kecamatan

    if kabupaten:
        update_data["kabupaten"] = kabupaten

    if provinsi:
        update_data["provinsi"] = provinsi
    
    if provinsi:
        update_data["kode_pos"] = kode_pos

    await collection.update_one(
        {"_id": object_id},
        {"$set": update_data},
    )

    document = await collection.find_one({"_id": object_id})

    return {"message": "Data updated successfully", "updated_data": update_data}

async def delete_sanggar_data(id: str):
    object_id = ObjectId(id)

    sanggar_image = []

    cursor = collection.find({"_id": object_id})

    async for document in cursor:
        sanggar_image_data = document["image"]
        
        sanggar_image.append(sanggar_image_data)

    for path_todelete_sanggar in sanggar_image:
        if os.path.exists(path_todelete_sanggar):
            os.remove(path_todelete_sanggar)
            print(f"The file {path_todelete_sanggar} has been deleted.")
        else:
            print(f"The file {path_todelete_sanggar} does not exist.")

    await collection.delete_one({"_id": object_id})

    return True
        
async def update_sanggar_photo(id: str, foto: str):
    object_id = ObjectId(id)
    await collection.update_one({"_id": object_id}, {"$set":{"image": foto}})
    document = await collection.find_one({"_id": object_id})
    return document
