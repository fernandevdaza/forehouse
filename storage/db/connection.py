from beanie import init_beanie, Document
from motor.motor_asyncio import AsyncIOMotorClient


async def init_connection(uri: str, db_name: str):

    client = AsyncIOMotorClient(uri)
    db = client[db_name]
    await init_beanie(database=db, document_models=[])

