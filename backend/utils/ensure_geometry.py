from shapely.geometry import shape, Point, GeometryCollection, Polygon
from shapely.geometry.base import BaseGeometry


def ensure_geometry(geom):
    """
    Verifica si la geometría ya es una instancia de Shapely o si es necesario convertirla.
    """
    if isinstance(geom, BaseGeometry):
        return geom
    elif isinstance(geom, dict):
        return shape(geom)
    elif hasattr(geom, "type") and hasattr(geom, "coordinates"):
        return shape({"type": geom.type, "coordinates": geom.coordinates})
    else:
        raise ValueError(f"Tipo de geometría desconocido: {type(geom)}")
