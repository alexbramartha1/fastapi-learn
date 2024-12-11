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

collection_desa_list = database["desa-list"]
collection_kecamatan_list = database["kecamatan-list"]
collection_kabupaten_list = database["kabupaten-list"]
collection_provinsi_list = database["provinsi-list"]

async def fetch_desa_data():
    desa = []

    document = collection_desa_list.find({})

    async for list in document:
        data_desa = {
            "_id": str(list["_id"]),
            "nama_desa": list["nama_desa"],
            "kecamatan_id": list["kecamatan_id"]
        }

        desa.append(data_desa)

    return {"desa-data": desa}

async def fetch_desa_data_by_kecamatan_id(id: str):
    desa = []

    document = collection_desa_list.find({"kecamatan_id": id})

    async for list in document:
        data_desa = {
            "_id": str(list["_id"]),
            "nama_desa": list["nama_desa"],
            "kecamatan_id": list["kecamatan_id"]
        }

        desa.append(data_desa)

    return {"desa-data": desa}


async def fetch_kecamatan_data():
    kecamatan = []

    document = collection_kecamatan_list.find({})

    async for list in document:
        data_kecamatan = {
            "_id": str(list["_id"]),
            "nama_kecamatan": list["nama_kecamatan"],
            "kabupaten_id": list["kabupaten_id"]
        }

        kecamatan.append(data_kecamatan)

    return {"kecamatan-data": kecamatan}

async def fetch_kecamatan_data_by_kabupaten_id(id: str):
    kecamatan = []

    document = collection_kecamatan_list.find({"kabupaten_id": id})

    async for list in document:
        data_kecamatan = {
            "_id": str(list["_id"]),
            "nama_kecamatan": list["nama_kecamatan"],
            "kabupaten_id": list["kabupaten_id"]
        }

        kecamatan.append(data_kecamatan)

    return {"kecamatan-data": kecamatan}


async def fetch_kabupaten_data():
    kabupaten = []

    document = collection_kabupaten_list.find({})

    async for list in document:
        data_kabupaten = {
            "_id": str(list["_id"]),
            "nama_kabupaten": list["nama_kabupaten"],
            "provinsi_id": list["provinsi_id"]
        }

        kabupaten.append(data_kabupaten)

    return {"kabupaten-data": kabupaten}

async def fetch_kabupaten_data_by_provinsi_id(id: str):
    kabupaten = []

    document = collection_kabupaten_list.find({"provinsi_id": id})

    async for list in document:
        data_kabupaten = {
            "_id": str(list["_id"]),
            "nama_kabupaten": list["nama_kabupaten"],
            "provinsi_id": list["provinsi_id"]
        }

        kabupaten.append(data_kabupaten)

    return {"kabupaten-data": kabupaten}

async def fetch_alamat_by_id_desa(id: str):
    objectId = ObjectId(id)
    desaListArray = []
    kecamatanListArray = []
    kabupatenListArray = []
    
    document = await collection_desa_list.find_one({"_id": objectId})

    if document:
        id_kec_in_desa = document["kecamatan_id"]

        documentDesa = collection_desa_list.find({"kecamatan_id": id_kec_in_desa})
        async for desaList in documentDesa:
            desaData = {
                "_id": str(desaList["_id"]),
                "nama_desa": desaList["nama_desa"],
                "kecamatan_id": desaList["kecamatan_id"]
            }

            desaListArray.append(desaData)

        objectKecId = ObjectId(id_kec_in_desa)
        documentKecamatan = await collection_kecamatan_list.find_one({"_id": objectKecId})

        # Mendapatkan list kecamatan berdasarkan kabupaten ID
        id_kab_in_kec = documentKecamatan["kabupaten_id"]
        documentKecamatanList = collection_kecamatan_list.find({"kabupaten_id": id_kab_in_kec})
        async for kecamatanList in documentKecamatanList:
            kecamatanData = {
                "_id": str(kecamatanList["_id"]),
                "nama_kecamatan": kecamatanList["nama_kecamatan"],
                "kabupaten_id": kecamatanList["kabupaten_id"]
            }

            kecamatanListArray.append(kecamatanData)

        return {
            "desa_data": desaListArray,
            "kecamatan_data": kecamatanListArray,
            "kabupaten_id": id_kab_in_kec
        }
    
    return None
    
