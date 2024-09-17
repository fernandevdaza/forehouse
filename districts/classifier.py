from pykml import parser
from shapely.geometry import Point
import geopandas as gpd
import matplotlib.pyplot as plt

kml_file = './districts/datos/Barrios de Santa Cruz de la Sierra/doc.kml'

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

print("CRS de los puntos:", puntos_gdf.crs)
print("CRS de los distritos:", all_districts_gdf.crs)

if puntos_gdf.crs != all_districts_gdf.crs:
    puntos_gdf = puntos_gdf.to_crs(all_districts_gdf.crs)

print("Primeros puntos cargados:\n", puntos_gdf.head())

puntos_clasificados = gpd.sjoin(puntos_gdf, all_districts_gdf, how="left", predicate="within")

print("Clasificación de puntos:\n", puntos_clasificados[['nombre', 'distrito']])

puntos_clasificados[['nombre', 'distrito', 'geometry']].to_file('./districts/datos/puntos_clasificados.geojson', driver='GeoJSON')

base = all_districts_gdf.plot(color='white', edgecolor='black')
puntos_gdf.plot(ax=base, marker='o', color='red', markersize=200)  # Ajuste del tamaño de los puntos

plt.show()
