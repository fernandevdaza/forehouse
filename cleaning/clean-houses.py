import json

# Función recursiva para desanidar cualquier campo anidado
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], name + a + '_')
        elif isinstance(x, list):
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

# Función para convertir ciertos campos a float
def convert_fields_to_float(house, i):
    # Convertir el campo 'price' a float
    try:
        if house['currency'] == 'USD':
            house['price'] = float(house['price'])
        elif house['currency'] == 'BOB':
            house['price'] = round((float(house['price']) / 6.96), 2)
            house['currency'] = 'USD'
    except (ValueError, KeyError):
        with open('errors.txt', 'a', encoding='utf-8') as f:
            f.write(f"Error en la línea {i}: price\n")

    # Convertir los campos de lat y lng a float si existen
    if 'location_lat' in house:
        try:
            house['location_lat'] = float(house['location_lat'])
        except (ValueError, KeyError):
            with open('errors.txt', 'a', encoding='utf-8') as f:
                f.write(f"Error en la línea {i}: location_lat\n")

    if 'location_lng' in house:
        try:
            house['location_lng'] = float(house['location_lng'])
        except (ValueError, KeyError):
            with open('errors.txt', 'a', encoding='utf-8') as f:
                f.write(f"Error en la línea {i}: location_lng\n")

# Función para limpiar y desanidar los datos de las casas
def clean_and_flatten_houses(jsonl):
    for i, line in jsonl:
        try:
            house = json.loads(line)
        except json.JSONDecodeError:
            with open('errors.txt', 'a', encoding='utf-8') as f:
                f.write(f"Error en la línea {i}: No se pudo decodificar el JSON\n")
            continue

        # Desanidar todo el JSON
        flattened_house = flatten_json(house)

        # Convertir los campos específicos a float o int
        convert_fields_to_float(flattened_house, i)

        # Guardar la casa limpiada y desanidada en un archivo nuevo sin escapado de caracteres Unicode
        with open('remax_flattened.jsonl', 'a', encoding='utf-8') as f2:
            f2.write(json.dumps(flattened_house, ensure_ascii=False) + '\n')


# Leer archivo y pasar a la función
with open('cleaning/houses.jsonl', 'r', encoding='utf-8') as f:
    # Leer el archivo línea por línea y enumerarlas
    jsonl = list(enumerate(f))
    # Llamar a la función para limpiar y desanidar los datos
    clean_and_flatten_houses(jsonl)
