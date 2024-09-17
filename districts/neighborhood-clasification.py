from pykml import parser
from shapely.geometry import Point, Polygon
import geopandas as gpd

districts_path = [
    './districts/datos/Distrito 1/doc.kml',
    './districts/datos/Distrito 2/doc.kml',
    './districts/datos/Distrito 3/doc.kml',
    './districts/datos/Distrito 4/doc.kml',
    './districts/datos/Distrito 5/doc.kml',
    './districts/datos/Distrito 6/doc.kml',
    './districts/datos/Distrito 7/doc.kml',
    './districts/datos/Distrito 8/doc.kml',
    './districts/datos/Distrito 9/doc.kml',
    './districts/datos/Distrito 10/doc.kml',
    './districts/datos/Distrito 11/doc.kml',
    './districts/datos/Distrito 12/doc.kml',
    './districts/datos/Distrito 13/doc.kml',
    './districts/datos/Distrito 14/doc.kml',
    './districts/datos/Distrito 15/doc.kml'
]

gdfs = []

for kml_file in districts_path:
    with open(kml_file, 'r') as f:
        root = parser.parse(f).getroot()

    for placemark in root.findall(".//{http://www.opengis.net/kml/2.2}Placemark"):
        polygon_elem = placemark.find(".//{http://www.opengis.net/kml/2.2}Polygon")
        if polygon_elem is None:
            print(f"Ignorado: El {placemark.find('.//{http://www.opengis.net/kml/2.2}name').text} no es un polígono.")
            continue

        nombre_distrito = placemark.find(".//{http://www.opengis.net/kml/2.2}name").text
        coordinates = polygon_elem.find(".//{http://www.opengis.net/kml/2.2}coordinates").text.strip().split()

        coords = [(float(coord.split(',')[0]), float(coord.split(',')[1])) for coord in coordinates]

        if len(coords) < 4:
            print(f"Advertencia: El polígono del {nombre_distrito} tiene menos de 4 puntos y no es válido.")
            continue

        if coords[0] != coords[-1]:
            coords.append(coords[0])

        try:
            polygon = Polygon(coords)
            gdf = gpd.GeoDataFrame({'distrito': [nombre_distrito], 'geometry': [polygon]}, crs="EPSG:4326")

            gdfs.append(gdf)
        except ValueError as e:
            print(f"Error al crear el polígono para {nombre_distrito}: {e}")

if gdfs:
    all_districts_gdf = gpd.pd.concat(gdfs, ignore_index=True)

    print(all_districts_gdf)

    all_districts_gdf.to_file('./districts/datos/distritos.geojson', driver='GeoJSON')
