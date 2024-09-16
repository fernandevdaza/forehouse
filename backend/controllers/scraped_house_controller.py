import numpy as np
from beanie import PydanticObjectId
from fastapi import HTTPException

from backend.models.neighborhood import Neighborhood
from backend.models.scraped_house import ScrapedHouse, ScrapedHouseResponse, ScrapedHouseInput
from typing import List


class ScrapedHouseController:
    def __init__(self):
        pass

    @classmethod
    async def retrieve_scraped_houses(cls) -> List[ScrapedHouseResponse]:
        scraped_houses = await ScrapedHouse.find_all().to_list()
        return [ScrapedHouseResponse(**scraped_house.model_dump()) for scraped_house in scraped_houses]

    @classmethod
    async def insert_scraped_house(cls, scraped_house: ScrapedHouseInput) -> ScrapedHouse:
        scraped_house = ScrapedHouse(**scraped_house.model_dump())

        district_id, neighborhood_id, district_name, neighborhood_name = await ScrapedHouse.get_district_and_neighborhood(
            scraped_house.location_lat, scraped_house.location_lng)

        scraped_house.district_id = district_id
        scraped_house.neighborhood_id = neighborhood_id
        scraped_house.neighborhood_name = neighborhood_name
        scraped_house.district_name = district_name

        await scraped_house.create()

        return await scraped_house

    async def get_location_info(lat: float, lng: float):
        """Obtener información del distrito y vecindario a partir de las coordenadas."""
        try:
            district_id, neighborhood_id, district_name, neighborhood_name = await ScrapedHouse.get_district_and_neighborhood(
                lat, lng)
            if district_id is None or neighborhood_id is None:
                raise HTTPException(status_code=404,
                                    detail="No se encontró un distrito o vecindario para la ubicación proporcionada.")
            return {
                "district_id": district_id,
                "neighborhood_id": neighborhood_id,
                "district_name": district_name,
                "neighborhood_name": neighborhood_name
            }
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))


