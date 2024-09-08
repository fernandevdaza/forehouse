from pykml import parser
from shapely.geometry import Point
import geopandas as gpd
import asyncio
from shapely.geometry import mapping
from backend.storage.db.connection import init_connection  # Tu módulo de conexión
from backend.storage.models.district import District       # Modelo del distrito
from backend.storage.models.neighborhood import Neighborhood  # Modelo del barrio
from config import CONFIG

DATABASE_URI = CONFIG.mongo_uri
DATABASE_NAME = CONFIG.mongo_name


# Función para insertar los barrios clasificados en la base de datos
async def insert_neighborhoods():
    await init_connection(DATABASE_URI, DATABASE_NAME)

    # Ruta al archivo KML con los puntos
    kml_file = './data/Barrios de Santa Cruz de la Sierra/doc.kml'

    # Cargar el archivo KML con los puntos
    with open(kml_file, 'r') as f:
        root = parser.parse(f).getroot()

    # Crear una lista para almacenar los puntos
    puntos = []
    nombres_puntos = []

    # Extraer los puntos del archivo KML
    for placemark in root.findall(".//{http://www.opengis.net/kml/2.2}Placemark"):
        point_elem = placemark.find(".//{http://www.opengis.net/kml/2.2}Point")
        if point_elem is not None:
            coordinates = point_elem.find(".//{http://www.opengis.net/kml/2.2}coordinates").text.strip().split(',')
            nombre_punto = placemark.find(".//{http://www.opengis.net/kml/2.2}name").text
            punto = Point(float(coordinates[0]), float(coordinates[1]))

            # Almacenar el punto y su nombre
            puntos.append(punto)
            nombres_puntos.append(nombre_punto)

    # Crear un GeoDataFrame con los puntos
    puntos_gdf = gpd.GeoDataFrame({'nombre': nombres_puntos, 'geometry': puntos}, crs="EPSG:4326")

    # Cargar el archivo distritos.geojson
    all_districts_gdf = gpd.read_file('./data/distritos.geojson')

    # Asegurarse de que ambos GeoDataFrames tienen el mismo sistema de coordenadas
    if puntos_gdf.crs != all_districts_gdf.crs:
        puntos_gdf = puntos_gdf.to_crs(all_districts_gdf.crs)

    # Hacer una unión espacial (sjoin) para encontrar a qué distrito pertenece cada punto
    puntos_clasificados = gpd.sjoin(puntos_gdf, all_districts_gdf, how="left", predicate="within")

    # Iterar sobre los puntos clasificados y crear documentos para insertar en MongoDB
    for idx, row in puntos_clasificados.iterrows():
        if row['index_right'] is not None:  # Verificar que no sea None
            # Obtener el distrito correspondiente de MongoDB usando el nombre del distrito
            district = await District.find_one({"nombre": row['distrito']})

            if district:
                # Crear el documento del barrio con el ObjectId del distrito
                neighborhood = Neighborhood(
                    nombre=row['nombre'],
                    geometry=mapping(row['geometry']),
                    district_id=district.id  # Relacionar con el distrito usando el ObjectId
                )
                await neighborhood.insert()

    print("Barrios clasificados insertados en la base de datos.")


# Ejecutar la inserción de datos en la base de datos
asyncio.run(insert_neighborhoods())










