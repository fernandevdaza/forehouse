import geopandas as gpd
import asyncio
from shapely.geometry import mapping

from backend.storage.db.connection import init_connection
from backend.storage.models.district import District
from config import CONFIG


DATABASE_URI = CONFIG.mongo_uri
DATABASE_NAME = CONFIG.mongo_name

gdf = gpd.read_file('./data/distritos.geojson')


async def insert_districts():
    await init_connection(DATABASE_URI, DATABASE_NAME)

    for _, row in gdf.iterrows():
        district = District(
            nombre=row['distrito'],
            geometry=mapping(row['geometry'])
        )
        await district.insert()

asyncio.run(insert_districts())
