from pykml import parser
from shapely.geometry import Point
import geopandas as gpd
import asyncio
from shapely.geometry import mapping
from backend.db.connection import init_connection  # Tu módulo de conexión
from backend.models.district import District       # Modelo del distrito
from backend.models.neighborhood import Neighborhood  # Modelo del barrio
from config import CONFIG

DATABASE_URI = CONFIG.mongo_uri
DATABASE_NAME = CONFIG.mongo_name


async def insert_neighborhoods():
    await init_connection(DATABASE_URI, DATABASE_NAME)

    kml_file = 'Barrios de Santa Cruz de la Sierra/doc.kml'

    with open(kml_file, 'r') as f:
        root = parser.parse(f).getroot()

    puntos = []
    nombres_puntos = []

    for placemark in root.findall(".//{http://www.opengis.net/kml/2.2}Placemark"):
        point_elem = placemark.find(".//{http://www.opengis.net/kml/2.2}Point")
        if point_elem is not None:
            coordinates = point_elem.find(".//{http://www.opengis.net/kml/2.2}coordinates").text.strip().split(',')
            nombre_punto = placemark.find(".//{http://www.opengis.net/kml/2.2}name").text
            punto = Point(float(coordinates[0]), float(coordinates[1]))

            puntos.append(punto)
            nombres_puntos.append(nombre_punto)

    puntos_gdf = gpd.GeoDataFrame({'nombre': nombres_puntos, 'geometry': puntos}, crs="EPSG:4326")

    all_districts_gdf = gpd.read_file('./districts/datos/distritos.geojson')

    if puntos_gdf.crs != all_districts_gdf.crs:
        puntos_gdf = puntos_gdf.to_crs(all_districts_gdf.crs)

    puntos_clasificados = gpd.sjoin(puntos_gdf, all_districts_gdf, how="left", predicate="within")

    for idx, row in puntos_clasificados.iterrows():
        if row['index_right'] is not None:
            district = await District.find_one({"nombre": row['distrito']})

            if district:
                neighborhood = Neighborhood(
                    nombre=row['nombre'],
                    geometry=mapping(row['geometry']),
                    district_id=district.id
                )
                await neighborhood.insert()

    print("Barrios clasificados insertados en la base de datos.")


asyncio.run(insert_neighborhoods())










