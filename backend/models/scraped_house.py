from pydantic import BaseModel, Field
from beanie import Document
from typing import Optional, Dict
from backend.models.district import District
from backend.models.neighborhood import Neighborhood
from shapely.geometry import Point, shape
from bson import ObjectId
from backend.utils.ensure_geometry import ensure_geometry


class ScrapedHouseResponse(BaseModel):
    """Scraped House response representation"""
    title: str
    price: float
    currency: str
    location_address: str
    location_city: str
    location_state: str
    location_lat: float
    location_lng: float
    characteristics_bedrooms: int
    characteristics_bathrooms: int
    characteristics_garages: int
    characteristics_area: float
    description: str
    url: str


class ScrapedHouseInput(BaseModel):
    """Scraped House input representation (flat structure, accepts dynamic fields)"""
    title: str
    price: float
    currency: str
    location_address: str
    location_city: str
    location_state: str
    location_lat: float
    location_lng: float
    characteristics_bedrooms: int
    characteristics_bathrooms: int
    characteristics_garages: Optional[int] = 0
    characteristics_area: float
    description: Optional[str] = ""
    url: str

    class Config:
        extra = "allow"


class ScrapedHouse(Document):
    """Scraped House representation with dynamic fields (flat structure)"""
    title: str
    price: float
    currency: str
    location_address: str
    location_city: str
    location_state: str
    location_lat: float
    location_lng: float
    characteristics_bedrooms: int
    characteristics_bathrooms: int
    characteristics_garages: int
    characteristics_area: float
    description: str
    url: str

    district_id: Optional[ObjectId] = None
    district_name: Optional[str] = None
    neighborhood_id: Optional[ObjectId] = None
    neighborhood_name: Optional[str] = None

    class Settings:
        collection = "scraped_houses"

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"  # Permitir campos adicionales no definidos explícitamente en el modelo

    def __repr__(self):
        return f"{self.title} - {self.price} {self.currency}"

    @classmethod
    async def get_district_and_neighborhood(cls, location_lat: float, location_lng: float):
        all_districts = await District.find_all().to_list()
        all_neighborhoods = await Neighborhood.find_all().to_list()

        house_point = Point(location_lng, location_lat)

        district_id = None
        neighborhood_id = None
        district_name = None
        neighborhood_name = None

        # Iterar sobre los distritos
        for district in all_districts:
            district_geom = ensure_geometry(district.geometry)

            # Si el distrito contiene el punto de la casa
            if district_geom.contains(house_point):
                district_id = district.id  # Usar ObjectId directamente
                district_name = district.nombre

                # Inicializar el vecindario más cercano y la distancia mínima
                closest_neighborhood = None
                min_distance = float("inf")

                # Iterar sobre los vecindarios dentro del distrito
                for neighborhood in all_neighborhoods:
                    if neighborhood.district_id == district.id:
                        neighborhood_geom = ensure_geometry(neighborhood.geometry).centroid
                        distance = house_point.distance(neighborhood_geom)

                        if distance < min_distance:
                            min_distance = distance
                            closest_neighborhood = neighborhood

                # Si se encontró un vecindario cercano, asignar el ID
                if closest_neighborhood:
                    neighborhood_id = closest_neighborhood.id  # Usar ObjectId directamente
                    neighborhood_name = closest_neighborhood.nombre
                break

        return district_id, neighborhood_id, district_name, neighborhood_name

