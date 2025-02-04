from models.gamelanbali import *
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
from typing import List

uri = "mongodb://alexbramartha14:WCknO6oCCiM8r3qC@tagamelanbaliakhir-shard-00-00.zx7dr.mongodb.net:27017,tagamelanbaliakhir-shard-00-01.zx7dr.mongodb.net:27017,tagamelanbaliakhir-shard-00-02.zx7dr.mongodb.net:27017/?ssl=true&replicaSet=atlas-qfuxr3-shard-0&authSource=admin&retryWrites=true&w=majority&appName=TAGamelanBaliAkhir"
client = AsyncIOMotorClient(uri)

database = client["tugas-akhir-data"]

collectionNode = database["note-admin"]

async def getNote(id: str):

    response = await collectionNode.find_one({"id_data": id})

    if response:
        dataInsert = {
            "_id": str(response["_id"]),
            "note": response["note"],
            "id_data": response["id_data"],
            "id_status": response["id_status"]
        }

        return dataInsert

async def createNote(note: str, idData: str, idStatus: str):
    
    if note and idData and idStatus:
        dataNote = {
            "note": note,
            "id_data": idData,
            "id_status": idStatus
        }

        response = await collectionNode.insert_one(dataNote)

        if response.inserted_id:
            return {"_id": str(response.inserted_id), "status": "Successfully added note!"}

async def updateNote(idData: str, note: str = None, idStatus: str = None):
    updatedData = {}

    if note:
        updatedData["note"] = note
    
    if idStatus:
        updatedData["id_status"] = idStatus
    
    response = await collectionNode.update_one({"id_data": idData}, {"$set": updatedData})

    if response:
        return {"message": "Data updated successfully", "updated_data": updatedData}
    
async def deleteNote(id: str):
    responseDelete = await collectionNode.delete_one({"id_data": id})
    if responseDelete:
        return True