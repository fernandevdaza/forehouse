import motor.motor_asyncio
from beanie import Document, init_beanie
from pydantic import BaseModel
from typing import List


class Geometry(BaseModel):
    type: str
    coordinates: List


class District(Document):
    nombre: str
    geometry: Geometry

    class Settings:
        collection = "districts"
