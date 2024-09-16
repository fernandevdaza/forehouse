import pandas as pd
import json
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder

# Leer el archivo JSON
json_data_path = 'prediction/ultracasas-final.json'

with open(json_data_path, 'r', encoding='utf-8') as file:
    json_data = file.read()

# Cargar el JSON como un diccionario de Python
data = json.loads(json_data)

# Normalizar el JSON en un DataFrame
df = pd.json_normalize(data)

# Eliminar columnas irrelevantes que no se pueden convertir en numéricas
df = df.drop(columns=[
    'title', 'description', 'url', 'location.address', 'location.city', 'location.state'
])

# Identificar columnas categóricas para codificar
categorical_columns = [
    'currency', 'extras.Estado', 'extras.Piscina', 'extras.Aire Acondicionado',
    'extras.Churrasqueras', 'extras.Comedor de Diario', 'extras.Dependencias de Servicio',
    'extras.Jardín', 'extras.Entrega', 'extras.Calefacción', 'extras.Baulera', 'extras.Gas Natural',
    'extras.Condominio Cerrado', 'extras.Club House', 'extras.Sala de Juegos', 'extras.Gimnasio',
    'extras.Preparada adultos mayores', 'extras.Preparada para accesibilidad', 'extras.Amoblado',
    'extras.Monoambiente', 'extras.Gastos Comunes'
]

# Aplicar LabelEncoder a las columnas categóricas y almacenar los codificadores para cada columna
encoders = {}
for column in categorical_columns:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column].astype(str))
    encoders[column] = le  # Guardamos el codificador para usarlo más tarde en predicción

# Verifica las clases de 'currency' para asegurarte de que 'USD' está incluido
print(f"Clases de 'currency': {encoders['currency'].classes_}")

# Verifica las columnas después de la codificación
print(df.dtypes)

# Separar las características (X) y la variable objetivo (y)
X = df.drop(columns=['price'])  # Eliminar la columna 'price' para que sea la variable objetivo
y = df['price']

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear y entrenar el modelo de XGBoost
model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.05, max_depth=5)
model.fit(X_train, y_train)

# Hacer predicciones
y_pred = model.predict(X_test)

# Calcular el error cuadrático medio
mse = mean_squared_error(y_test, y_pred)
print(f"Error cuadrático medio (MSE): {mse}")

# Predecir con un nuevo ejemplo JSON
new_data_json = '''
{
  "currency": "USD",
  "location.lat": -17.87220208,
  "location.lng": -63.12585346,
  "characteristics.bedrooms": 4,
  "characteristics.bathrooms": 2,
  "characteristics.area": 113.53,
  "characteristics.garages": 0,
  "extras.Estado": "NUEVO"
}
'''

# Cargar el nuevo ejemplo JSON como un diccionario de Python
new_data = json.loads(new_data_json)

# Convertir el nuevo JSON en un DataFrame para predicción
new_data_df = pd.json_normalize([new_data])

# Aplicar las mismas transformaciones a las columnas categóricas en el nuevo ejemplo
for column in categorical_columns:
    le = encoders[column]
    # Si el valor existe en el codificador, lo transformamos; si no, lanzamos un aviso
    try:
        new_data_df[column] = le.transform(new_data_df[column].astype(str))
    except KeyError as e:
        print(f"Valor no encontrado en el LabelEncoder para {column}: {e}")
        new_data_df[column] = -1  # O manejarlo de otra manera

# Asegurarse de que todas las columnas del conjunto de entrenamiento estén en el conjunto de predicción
missing_cols = set(X_train.columns) - set(new_data_df.columns)
for col in missing_cols:
    # Rellenar con un valor por defecto, por ejemplo, 0 o NaN si es apropiado
    new_data_df[col] = 0  # Puedes cambiar a NaN o un valor que consideres adecuado

# Reordenar las columnas para que coincidan con el conjunto de entrenamiento
new_data_df = new_data_df[X_train.columns]

# Hacer predicción con el nuevo ejemplo
prediccion = model.predict(new_data_df)
print(f"Predicción del precio para la nueva casa: {prediccion[0]}")

