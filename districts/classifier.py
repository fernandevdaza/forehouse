from pykml import parser
from shapely.geometry import Point
import geopandas as gpd
import matplotlib.pyplot as plt

# Ruta al archivo KML con los puntos
kml_file = './districts/Barrios de Santa Cruz de la Sierra/doc.kml'

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
all_districts_gdf = gpd.read_file('./districts/distritos.geojson')

# Verificar el CRS de los puntos y los distritos
print("CRS de los puntos:", puntos_gdf.crs)
print("CRS de los distritos:", all_districts_gdf.crs)

# Si no tienen el mismo CRS, convertir los puntos al CRS de los distritos
if puntos_gdf.crs != all_districts_gdf.crs:
    puntos_gdf = puntos_gdf.to_crs(all_districts_gdf.crs)

# Verificar las primeras coordenadas de los puntos
print("Primeros puntos cargados:\n", puntos_gdf.head())

# Hacer una unión espacial (sjoin) para encontrar a qué distrito pertenece cada punto
puntos_clasificados = gpd.sjoin(puntos_gdf, all_districts_gdf, how="left", predicate="within")

# Mostrar los puntos con su distrito correspondiente
print("Clasificación de puntos:\n", puntos_clasificados[['nombre', 'distrito']])

# Guardar el resultado clasificado en un archivo GeoJSON
puntos_clasificados[['nombre', 'distrito', 'geometry']].to_file('./districts/puntos_clasificados.geojson', driver='GeoJSON')

# Graficar los distritos y los puntos con un tamaño visible
base = all_districts_gdf.plot(color='white', edgecolor='black')
puntos_gdf.plot(ax=base, marker='o', color='red', markersize=200)  # Ajuste del tamaño de los puntos

# Mostrar el gráfico
plt.show()
