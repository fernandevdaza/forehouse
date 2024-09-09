from pydantic import Field
from beanie import Document
from pydantic import BaseModel
from typing import Optional
from backend.models.district import District
from backend.models.neighborhood import Neighborhood
from shapely.geometry import Point, shape

from backend.utils.ensure_geometry import ensure_geometry


class LocationScrapedHouse(BaseModel):
    """Location representation"""
    address: str
    city: str
    state: str
    lat: float
    lng: float


class ScrapedHouseResponse(BaseModel):
    """Scraped House response representation"""
    title: str
    price: int
    currency: str
    description: str
    url: str


class ScrapedHouseInput(BaseModel):
    """Scraped House input representation"""
    title: str
    price: int
    currency: str
    location: LocationScrapedHouse
    characteristics: dict
    extras: dict
    description: str
    url: str


class ScrapedHouse(Document):
    """Scraped House representation"""
    title: str
    price: int
    currency: str
    location: LocationScrapedHouse
    characteristics: dict
    extras: dict
    description: str
    url: str
    neighborhood_id: Optional[str] = None
    district_id: Optional[str] = None

    def __repr__(self):
        return f"{self.title} - {self.price} {self.currency}"

    class Settings:
        collection = "scraped_houses"

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    async def get_district_and_neighborhood(cls, location: LocationScrapedHouse):
        all_districts = await District.find_all().to_list()
        all_neighborhoods = await Neighborhood.find_all().to_list()

        house_point = Point(location.lng, location.lat)

        district_id = None
        neighborhood_id = None

        for district in all_districts:
            print(f"Tipo de geometría del distrito: {type(district.geometry)}")  # Depuración: Imprimir el tipo de geometría
            print(f"Contenido de la geometría del distrito: {district.geometry}")  # Depuración: Ver el contenido real
            district_geom = ensure_geometry(district.geometry)  # Verificar si la geometría ya es válida

            if district_geom.contains(house_point):  # Si el distrito contiene el punto
                district_id = str(district.id)  # Guardar el ID del distrito
                closest_neighborhood = None
                min_distance = float("inf")

            for neighborhood in all_neighborhoods:
                    if neighborhood.district_id == district.id:
                        neighborhood_geom = ensure_geometry(
                            neighborhood.geometry).centroid
                        distance = house_point.distance(neighborhood_geom)

                        if distance < min_distance:
                            min_distance = distance
                            closest_neighborhood = neighborhood

            if closest_neighborhood:
                neighborhood_id = str(closest_neighborhood.id)
            break

        return district_id, neighborhood_id

