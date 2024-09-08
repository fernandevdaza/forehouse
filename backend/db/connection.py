from beanie import init_beanie, Document
from motor.motor_asyncio import AsyncIOMotorClient
from backend.storage.models.district import District
from backend.storage.models.neighborhood import Neighborhood

async def init_connection(uri: str, db_name: str):

    client = AsyncIOMotorClient(uri)
    db = client[db_name]
    await init_beanie(database=db, document_models=[District, Neighborhood])

