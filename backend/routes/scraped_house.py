"""Scraped Houses Router"""

from datetime import datetime, UTC
from typing import List

from fastapi import APIRouter, Body, HTTPException

from backend.models.scraped_house import ScrapedHouse, ScrapedHouseResponse, ScrapedHouseInput
from backend.controllers.scraped_house_controller import ScrapedHouseController

router = APIRouter(prefix='/scraped_houses', tags=['Scraped Houses'])

embed = Body(..., embed=True)


@router.post("/insert_one", response_model=ScrapedHouseResponse)
async def insert_scraped_house(scraped_house: ScrapedHouseInput):
    """Insert a new scraped house"""
    scraped_house_created = await ScrapedHouseController.insert_scraped_house(scraped_house)

    return ScrapedHouseResponse(
        title=scraped_house_created.title,
        price=scraped_house_created.price,
        currency=scraped_house_created.currency,
        description=scraped_house_created.description,
        url=scraped_house_created.url
    )


@router.post("/insert_many", response_model=List[ScrapedHouseResponse])
async def insert_scraped_houses(scraped_houses: List[ScrapedHouseInput]):
    """Insert multiple scraped houses"""
    responses = []

    for scraped_house_input in scraped_houses:
        scraped_house = await ScrapedHouseController.insert_scraped_house(scraped_house_input)
        responses.append(ScrapedHouseResponse(
            title=scraped_house.title,
            price=scraped_house.price,
            currency=scraped_house.currency,
            description=scraped_house.description,
            url=scraped_house.url
        ))

    if not responses:
        raise HTTPException(status_code=400,
                            detail="Ninguna casa fue insertada debido a que no se encontró un distrito o vecindario válido.")

    return responses


@router.get("/get_location_info")
async def get_location_info(lat: float, lng: float):
    """Obtener información del distrito y vecindario a partir de las coordenadas."""
    try:
        location_info = await ScrapedHouseController.get_location_info(lat, lng)
        return location_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_scraped_houses", response_model=List[ScrapedHouseResponse])
async def get_scraped_houses():
    """Get all neighborhoods"""
    try:
        scraped_houses = await ScrapedHouseController.retrieve_scraped_houses()
        return scraped_houses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

