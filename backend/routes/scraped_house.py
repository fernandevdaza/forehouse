"""Scraped Houses Router"""

from datetime import datetime, UTC

from fastapi import APIRouter, Body, Response, HTTPException

from backend.models.scraped_house import ScrapedHouse, ScrapedHouseResponse, ScrapedHouseInput

router = APIRouter(prefix='/scraped_houses', tags=['Scraped Houses'])

embed = Body(..., embed=True)


@router.post("", response_model=ScrapedHouseResponse)
async def insert_scraped_house(scraped_house: ScrapedHouseInput):
    """Insert a new scraped house"""
    scraped_house = ScrapedHouse(**scraped_house.model_dump())

    scraped_house.district_id, scraped_house.neighborhood_id = await ScrapedHouse.get_district_and_neighborhood(scraped_house.location)

    await scraped_house.create()

    return ScrapedHouseResponse(
        title=scraped_house.title,
        price=scraped_house.price,
        currency=scraped_house.currency,
        description=scraped_house.description,
        url=scraped_house.url
    )
