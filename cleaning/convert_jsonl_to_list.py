import json


# Función para convertir JSONL a JSON
def convertir_jsonl_a_json(archivo_jsonl, archivo_json):
    # Lista para almacenar los objetos JSON
    json_array = []

    # Abrir el archivo JSONL y leer línea por línea
    with open(archivo_jsonl, 'r', encoding='utf-8') as f:
        for linea in f:
            # Convertir la línea a un objeto JSON
            json_obj = json.loads(linea.strip())
            # Agregar el objeto a la lista
            json_array.append(json_obj)

    # Guardar la lista como un array en el archivo JSON
    with open(archivo_json, 'w', encoding='utf-8') as f:
        json.dump(json_array, f, indent=4, ensure_ascii=False)


# Uso del script
archivo_jsonl = 'cleaning/remax.jsonl'  # Nombre del archivo JSONL
archivo_json = 'remax-final.json'  # Nombre del archivo de salida JSON

convertir_jsonl_a_json(archivo_jsonl, archivo_json)
