from pydantic import Field
from bson import ObjectId
from beanie import Document
from typing import Optional


class Neighborhood(Document):
    nombre: str
    geometry: dict
    district_id: Optional[ObjectId] = Field(..., description="ID del distrito asociado")

    class Settings:
        collection = "neighborhoods"

    class Config:
        arbitrary_types_allowed = True
