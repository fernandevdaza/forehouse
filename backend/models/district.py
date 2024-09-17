from pydantic import BaseModel, Field, ConfigDict
from beanie import PydanticObjectId, Document
from typing import List
from backend.models.neighborhood import NeighborhoodOutput


class Geometry(BaseModel):
    type: str
    coordinates: List


class DistrictAndNeighborhood(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")  # Asegúrate de mapear correctamente el campo "_id"
    nombre: str
    geometry: Geometry
    neighborhoods: List[NeighborhoodOutput]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True,
        populate_by_name=True
    )


class DistrictOutput(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")  # Asegúrate de mapear correctamente el campo "_id"
    nombre: str
    geometry: Geometry

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True,
        populate_by_name=True
    )


class District(Document):
    nombre: str
    geometry: Geometry

    class Settings:
        collection = "districts"
