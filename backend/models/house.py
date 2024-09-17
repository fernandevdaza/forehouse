from beanie import Document, PydanticObjectId
from pydantic import BaseModel
from typing import Optional


# HouseInput as a Pydantic model
class HouseInput(BaseModel):
    _id: Optional[PydanticObjectId] = None
    bedrooms: int = 0
    bathrooms: int = 0
    garages: int = 0
    built_area: float = 0.0
    terrain_area: float = 0.0
    lat: Optional[float] = None
    lng: Optional[float] = None
    neighborhood_id: Optional[PydanticObjectId] = None
    district_id: Optional[PydanticObjectId] = None


# Prices as a Pydantic model
class Prices(BaseModel):
    from_price_model: float
    from_no_price_model: float
    final_predicted_price: float

# HouseOutput como un modelo de Pydantic
class HouseOutput(BaseModel):
    _id: PydanticObjectId
    bedrooms: int
    bathrooms: int
    garages: int
    built_area: float
    terrain_area: float
    lat: float
    lng: float
    neighborhood_id: Optional[PydanticObjectId] = None
    district_id: Optional[PydanticObjectId] = None
    prices: Prices  # Campo 'prices' que incluye el objeto Prices
    neighborhood_name: Optional[str] = None
    price_per_m2: Optional[float] = None




# Main House class in Beanie
class House(Document):
    bedrooms: int
    bathrooms: int
    garages: int
    built_area: float
    terrain_area: float
    lat: float
    lng: float
    neighborhood_id: Optional[PydanticObjectId] = None
    district_id: Optional[PydanticObjectId] = None
    prices: Prices

    class Settings:
        collection = "houses"
