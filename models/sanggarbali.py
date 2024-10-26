from pydantic import BaseModel
from bson import ObjectId

class SanggarData(BaseModel):
    _id: str
    image: str
    nama_sanggar: str
    alamat: str
    no_telepon: str
    latitude: str = None
    longitude: str = None
    id_creator: str

    class Config:
        from_attributes = True  # Jika ada integrasi dengan ORM di masa depan
