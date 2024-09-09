from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from backend.models.district import District
from backend.models.neighborhood import Neighborhood
from backend.models.scraped_house import ScrapedHouse

async def init_connection(uri: str, db_name: str):

    client = AsyncIOMotorClient(uri)
    db = client[db_name]
    await init_beanie(database=db, document_models=[District, Neighborhood, ScrapedHouse])

