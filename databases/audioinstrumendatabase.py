from models.audiogamelanbali import *
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import json
from fastapi import FastAPI, HTTPException
import re
import time
from datetime import datetime
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

uri = "mongodb://alexbramartha14:WCknO6oCCiM8r3qC@tagamelanbaliakhir-shard-00-00.zx7dr.mongodb.net:27017,tagamelanbaliakhir-shard-00-01.zx7dr.mongodb.net:27017,tagamelanbaliakhir-shard-00-02.zx7dr.mongodb.net:27017/?ssl=true&replicaSet=atlas-qfuxr3-shard-0&authSource=admin&retryWrites=true&w=majority&appName=TAGamelanBaliAkhir"
client = AsyncIOMotorClient(uri)

database = client["tugas-akhir-data"]

collection_audio_instrumen = database["audio-instrumen"]

async def create_audio_data_instrumen(audio_name: str, audio_path: str, instrument_id: str):

    audio_data = {
        "instrument_id": instrument_id,
        "audio_name": audio_name,
        "audio_path": audio_path
    }
    
    response = await collection_audio_instrumen.insert_one(audio_data)

    return {"_id": str(response.inserted_id), "audio_data": audio_name, "message": "Data created successfully"}


async def fetch_audio_by_instrumen_id(id: str):
    response = collection_audio_instrumen.find({"instrument_id": id})
    
    audio_array = []

    async for audio_data in response:
        audio_data_input = {
            "_id": str(audio_data["_id"]),
            "audio_name": audio_data["audio_name"],
            "audio_path": audio_data["audio_path"]
        }

        audio_array.append(audio_data_input)

    return {
        "audio_array": audio_array
    }

async def fetch_all_audio_instrumen():

    response = collection_audio_instrumen.find({})
    
    audio_array = []

    async for audio_data in response:
        audio_data_input = {
            "_id": str(audio_data["_id"]),
            "audio_name": audio_data["audio_name"],
            "audio_path": audio_data["audio_path"],
            "instrument_id": audio_data["instrument_id"]
        }

        audio_array.append(audio_data_input)

    return {
        "audio_array": audio_array
    }


async def fetch_audio_path_instrumen(id: str):
    object_id = ObjectId(id)
    document = await collection_audio_instrumen.find_one({"_id": object_id})
    audio_path = document.get("audio_path")
    return audio_path

async def delete_audio_instrumen_data(id: List[str]):
    object_id = []
    audio_file = []

    for id_data in id:  
        data_id_full = ObjectId(id_data)
        object_id.append(data_id_full)
        
    cursor = collection_audio_instrumen.find({"_id": {"$in": object_id}})

    async for document in cursor:
        audiofile = document["audio_path"]

        audio_file.append(audiofile)

    for path_todelete_audio in audio_file:
        public_id = extract_public_id(path_todelete_audio)

        cloudinary.uploader.destroy(public_id)

    await collection_audio_instrumen.delete_many({"_id": {"$in": object_id}})

    return True

def extract_public_id(secure_url):
    pattern = r"/upload/(?:v\d+/)?(.+)\.\w+$"
    match = re.search(pattern, secure_url)
    if match:
        return match.group(1)
    else:
        return None

async def update_audio_instrumen_data(id: str, audio_name: str, audio_path: str):
    object_id = ObjectId(id)
    updated_data = {}
    
    if audio_name:
        updated_data["audio_name"] = audio_name

    if audio_path:
        updated_data["audio_path"] = audio_path

    await collection_audio_instrumen.update_one(
        {"_id": object_id}, 
        {"$set": updated_data}
    )
    
    return {"message": "Data updated successfully", "updated_data": updated_data}
 