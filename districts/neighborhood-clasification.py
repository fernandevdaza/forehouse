from pykml import parser
from shapely.geometry import Point, Polygon
import geopandas as gpd

# Ruta a los archivos KML
districts_path = [
    './data/Distrito 1/doc.kml',
    './data/Distrito 2/doc.kml',
    './data/Distrito 3/doc.kml',
    './data/Distrito 4/doc.kml',
    './data/Distrito 5/doc.kml',
    './data/Distrito 6/doc.kml',
    './data/Distrito 7/doc.kml',
    './data/Distrito 8/doc.kml',
    './data/Distrito 9/doc.kml',
    './data/Distrito 10/doc.kml',
    './data/Distrito 11/doc.kml',
    './data/Distrito 12/doc.kml',
    './data/Distrito 13/doc.kml',
    './data/Distrito 14/doc.kml',
    './data/Distrito 15/doc.kml'
]

# Lista para almacenar todos los GeoDataFrames
gdfs = []

for kml_file in districts_path:
    with open(kml_file, 'r') as f:
        root = parser.parse(f).getroot()

    for placemark in root.findall(".//{http://www.opengis.net/kml/2.2}Placemark"):
        # Verificar si el placemark es un polígono
        polygon_elem = placemark.find(".//{http://www.opengis.net/kml/2.2}Polygon")
        if polygon_elem is None:
            print(f"Ignorado: El {placemark.find('.//{http://www.opengis.net/kml/2.2}name').text} no es un polígono.")
            continue

        nombre_distrito = placemark.find(".//{http://www.opengis.net/kml/2.2}name").text
        coordinates = polygon_elem.find(".//{http://www.opengis.net/kml/2.2}coordinates").text.strip().split()

        # Convertir las coordenadas a un formato manejable por shapely
        coords = [(float(coord.split(',')[0]), float(coord.split(',')[1])) for coord in coordinates]

        # Verificar que el polígono tiene suficientes puntos
        if len(coords) < 4:
            print(f"Advertencia: El polígono del {nombre_distrito} tiene menos de 4 puntos y no es válido.")
            continue

        # Cerrar el polígono si no está cerrado
        if coords[0] != coords[-1]:
            coords.append(coords[0])

        try:
            # Crear un polígono con shapely y definir el CRS
            polygon = Polygon(coords)
            gdf = gpd.GeoDataFrame({'distrito': [nombre_distrito], 'geometry': [polygon]}, crs="EPSG:4326")

            # Acumular en la lista de GeoDataFrames
            gdfs.append(gdf)
        except ValueError as e:
            print(f"Error al crear el polígono para {nombre_distrito}: {e}")

# Concatenar todos los GeoDataFrames en uno solo
if gdfs:
    all_districts_gdf = gpd.pd.concat(gdfs, ignore_index=True)

    # Mostrar el GeoDataFrame completo
    print(all_districts_gdf)

    # Guardar el GeoDataFrame en un archivo GeoJSON con CRS definido
    all_districts_gdf.to_file('./data/distritos.geojson', driver='GeoJSON')
