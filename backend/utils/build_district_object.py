def build_district_object(districts, neighborhoods):
    """Builds a district object with its neighborhoods"""
    new_districts = []
    for district in districts:
        district_id_str = str(district.id)
        new_district = {
            "id": district_id_str,
            "nombre": district.nombre,
            "geometry": district.geometry,
            "neighborhoods": []
        }
        for neighborhood in neighborhoods:
            neighborhood_district_id_str = str(neighborhood.district_id)
            if neighborhood_district_id_str == district_id_str:
                new_district["neighborhoods"].append(neighborhood)
        new_districts.append(new_district)
    return new_districts
