from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from beanie import Document, PydanticObjectId


# Campo personalizado para manejar ObjectId
# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v, field=None):
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid ObjectId")
#         return str(v)

#     # Pydantic v2.x: Cambiar __modify_schema__ por __get_pydantic_json_schema__
#     @classmethod
#     def __get_pydantic_json_schema__(cls, schema, handler):
#         schema.update(type="string")
#         return schema


class NeighborhoodGeometry(BaseModel):
    type: str
    coordinates: List[float]


# Modelo de salida ajustado
class NeighborhoodOutput(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")  # Convertimos ObjectId a str
    nombre: str
    geometry: NeighborhoodGeometry
    district_id: Optional[PydanticObjectId] = Field(None, description="ID del distrito asociado")  # También convertido
    price_per_m2: Optional[float] = Field(None, description="Precio por metro cuadrado promedio en USD")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True,
        populate_by_name=True
    )


# Modelo adicional
class NeighborhoodPriceM2(BaseModel):
    neighborhood_name: str
    price_per_m2: float

    class Settings:
        collection = "neighborhoods_prices_m2"

    class Config:
        arbitrary_types_allowed = True


# Modelo de MongoDB ajustado
class Neighborhood(Document):
    nombre: str
    geometry: dict
    district_id: Optional[ObjectId] = Field(..., description="ID del distrito asociado")
    price_per_m2: Optional[float] = Field(None, description="Precio por metro cuadrado promedio en USD")

    class Settings:
        collection = "neighborhoods"

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    async def find_by_name(cls, name: str):
        return await cls.find_one({"nombre": name})
