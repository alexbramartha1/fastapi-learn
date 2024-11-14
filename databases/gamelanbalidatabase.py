from models.gamelanbali import *
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import json
from fastapi import FastAPI, HTTPException
import os

uri = "mongodb://alexbramartha14:WCknO6oCCiM8r3qC@tagamelanbaliakhir-shard-00-00.zx7dr.mongodb.net:27017,tagamelanbaliakhir-shard-00-01.zx7dr.mongodb.net:27017,tagamelanbaliakhir-shard-00-02.zx7dr.mongodb.net:27017/?ssl=true&replicaSet=atlas-qfuxr3-shard-0&authSource=admin&retryWrites=true&w=majority&appName=TAGamelanBaliAkhir"
client = AsyncIOMotorClient(uri)

database = client["tugas-akhir-data"]

collection = database["gamelan-bali"]
collection_instrumen = database["instrumen-gamelan"]

async def fetch_all_instrument_by_gamelan_array(name: str):
    
    gamelan_specific = collection.find({"nama_gamelan": {"$regex": f"(?i){name}"}})

    gamelan_data_spec = []

    instrument_id = []

    async for instrument in gamelan_specific:
        gamelan_data = {
            "_id": str(instrument["_id"]),
            "nama_gamelan": instrument["nama_gamelan"],
            "golongan": instrument["golongan"],
            "description": instrument["description"],
            "upacara": instrument["upacara"],
            "audio_gamelan": instrument["audio_gamelan"],
            "instrument_id": instrument["instrument_id"],
            "status": instrument["status"]
        }
        
        instrument_data_id = {
            "instrument_id": instrument["instrument_id"]
        }
        
        gamelan_data_spec.append(gamelan_data)
        instrument_id.append(instrument_data_id)

    print(instrument_id)

    array_id = []
    
    for id in instrument_id:
        for item in id["instrument_id"]:
            object_ids = ObjectId(item)
            array_id.append(object_ids)

    print(array_id)

    instrumen = collection_instrumen.find({"_id": {"$in": array_id}})
    
    data_instrumen = []
    
    async for dataInstrument in instrumen:
        instrumen_data = {
            "_id": str(dataInstrument["_id"]),
            "nama_instrument": dataInstrument["nama_instrument"],
            "description": dataInstrument["description"],
            "trid_image": dataInstrument["trid_image"],
            "fungsi": dataInstrument["fungsi"],
            "image_instrumen": dataInstrument["image_instrumen"]
        }

        data_instrumen.append(instrumen_data)

    if gamelan_data_spec:

        return {
            "gamelan_data": gamelan_data_spec,
            "instrument_data": data_instrumen
        }
    
    return f"There is no data gamelan with this name {name}"

async def fetch_all_gamelan():
    gamelan = []

    document = collection.find({})

    async for data in document:
        audio = []
        gamelan_data = {
            "_id": str(data["_id"]),
            "nama_gamelan": data["nama_gamelan"],
            "golongan": data["golongan"],
            "description": data["description"],
            "upacara": data["upacara"],
            "audio_gamelan": data["audio_gamelan"],
            "instrument_id": data["instrument_id"],
            "status": data["status"]
        }

        gamelan.append(gamelan_data)

        for data_audio in data["audio_gamelan"]:
            audio_data = {
                "audio_name": data_audio["audio_name"],
                "audio_path": data_audio["audio_path"]
            }

            audio.append(audio_data)

        print(audio)

    return gamelan

async def fetch_specific_gamelan(id: str):
    object_id = ObjectId(id)
    gamelan = []
    document = collection.find({"_id": object_id})

    async for data in document:
        gamelan_data = {
            "_id": str(data["_id"]),
            "nama_gamelan": data["nama_gamelan"],
            "golongan": data["golongan"],
            "description": data["description"],
            "upacara": data["upacara"],
            "audio_gamelan": data["audio_gamelan"],
            "instrument_id": data["instrument_id"],
            "status": data["status"]
        }

        gamelan.append(gamelan_data)
        gamelan_testing = GamelanData(**gamelan_data)
        nama_audio = [audio.audio_name for audio in gamelan_testing.audio_gamelan]
        print(nama_audio) 

    return gamelan


async def fetch_byname_gamelan(nama_gamelan: str):
    gamelan = []

    cursor = collection.find({"nama_gamelan": {"$regex": f"(?i){nama_gamelan}"}})
    
    async for data in cursor:
        gamelan_data = {
            "_id": str(data["_id"]),
            "nama_gamelan": data["nama_gamelan"],
            "golongan": data["golongan"],
            "description": data["description"],
            "upacara": data["upacara"],
            "audio_gamelan": data["audio_gamelan"],
            "instrument_id": data["instrument_id"],
            "status": data["status"]
        }

        gamelan.append(gamelan_data)
    
    return gamelan

async def create_gamelan_data(nama_gamelan: str, golongan: str, description: str, upacara: List[str], audio_gamelan: str, instrument_id: List[str]):
    try:
        # Parse and convert audio_gamelan JSON data to a list of Audio objects
        audio_gamelan_list = [Audio(**item) for item in json.loads(audio_gamelan)]
        
        # Convert each Audio object to a dictionary
        audio_gamelan_dicts = [audio.dict() for audio in audio_gamelan_list]

    except json.JSONDecodeError:
        raise HTTPException(400, "Invalid JSON format for audio_gamelan")

    print(audio_gamelan_dicts)

    gamelan_data = {
        "nama_gamelan": nama_gamelan,
        "golongan": golongan,
        "description": description,
        "upacara": upacara,
        "audio_gamelan": audio_gamelan_dicts,
        "instrument_id": instrument_id,
        "status": "unapproved"
    }
    
    response = await collection.insert_one(gamelan_data)

    return {"_id": str(response.inserted_id), "nama_gamelan": nama_gamelan, "message": "Data created successfully"}

async def approval_gamelan_data(id: str, status: str):
    object_id = ObjectId(id)

    if status == "approved":
        await collection.update_one({"_id": object_id}, {"$set": {"status": status}})

        return f"Data Gamelan Bali {status}"
    
    if status == "unapproved":
        await collection.update_one({"_id": object_id}, {"$set": {"status": status}})

        return f"Data Gamelan Bali {status}"

async def update_gamelan_data(id: str, nama_gamelan: str, golongan: str, description: str, audio_gamelan: str, instrument_id: List[str], upacara: List[str]):
    object_id = ObjectId(id)
    updated_data = {}

    if not audio_gamelan:
        audio_gamelan == None

    if audio_gamelan:
        try:
            # Parse and convert audio_gamelan JSON data to a list of Audio objects
            audio_gamelan_list = [Audio(**item) for item in json.loads(audio_gamelan)]
            
            audio_gamelan_list = [data for data in audio_gamelan_list if  (data.audio_name and data.audio_path) and (data.audio_name != "string" and data.audio_path != "string")]

            # Convert each Audio object to a dictionary
            audio_gamelan_dicts = [audio.dict() for audio in audio_gamelan_list]

        except json.JSONDecodeError:
            raise HTTPException(400, "Invalid JSON format for audio_gamelan")

        print(audio_gamelan_dicts)
    
    if instrument_id:
        instrument_id = [data for data in instrument_id if data and data != "string"]

    if not instrument_id:
        instrument_id = None  

    if upacara:
        upacara = [data for data in upacara if data and data != "string"]
    
    if not upacara:
        upacara = None

    print(audio_gamelan)
    print(instrument_id)
    print(upacara)

    if nama_gamelan:
        updated_data["nama_gamelan"] = nama_gamelan

    if golongan:
        updated_data["golongan"] = golongan

    if description:
        updated_data["description"] = description
    
    if upacara:
        updated_data["upacara"] = upacara
    
    if audio_gamelan:
        updated_data["audio_gamelan"] = audio_gamelan_dicts
    
    if instrument_id:
        updated_data["instrument_id"] = instrument_id

    print(updated_data)

    await collection.update_one(
        {"_id": object_id}, 
        {"$set": updated_data}
    )
    
    return {"message": "Data updated successfully", "updated_data": updated_data}
 
async def delete_gamelan_bali(id: str):
    object_id = ObjectId(id)

    audio_gamelan = []

    cursor = collection.find({"_id": object_id})

    async for document in cursor:
        audio_gamelan_data = document["audio_gamelan"]
        
        for audio in audio_gamelan_data:
            audio_data = audio["audio_path"]

            audio_gamelan.append(audio_data)

    for path_todelete_audio in audio_gamelan:
        if os.path.exists(path_todelete_audio):
            os.remove(path_todelete_audio)
            print(f"The file {path_todelete_audio} has been deleted.")
        else:
            print(f"The file {path_todelete_audio} does not exist.")

    await collection.delete_one({"_id": object_id})

    return True
