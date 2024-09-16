import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from xgboost import plot_importance
import numpy as np
from sklearn.preprocessing import LabelEncoder

# Cargar los datos del nuevo dataset
df = pd.read_csv('prediction/dataset_ready_to_go2.csv')

# Aplicar la transformación logarítmica al precio
df['log_price'] = np.log(df['price'])



# Seleccionar las nuevas columnas para el modelo, incluyendo las categóricas
features = ['characteristics_bedrooms', 'characteristics_bathrooms', 'characteristics_garages',
            'characteristics_area', 'location_lat', 'location_lng', 'extras_Terreno',
            'neighborhood_name', 'district_name']

# # Aplicar Label Encoding a las columnas categóricas (barrio y distrito)
le_neighborhood = LabelEncoder()
le_district = LabelEncoder()

df['neighborhood_name'] = le_neighborhood.fit_transform(df['neighborhood_name'])
df['district_name'] = le_district.fit_transform(df['district_name'])

# Definir X (características) e y (objetivo log_price)
X = df[features]
y = df['log_price']

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear el modelo XGBoost
xgb_model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)

# Entrenar el modelo
xgb_model.fit(X_train, y_train)

# Hacer predicciones en los datos de prueba
y_pred = xgb_model.predict(X_test)

# Calcular el error cuadrático medio (MSE) para evaluar el modelo
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5

print(f'Error cuadrático medio (MSE): {mse}')
print(f'Raíz del error cuadrático medio (RMSE): {rmse}')

# Predecir con un nuevo ejemplo (casa específica)
casa_nueva = pd.DataFrame({
    'characteristics_bedrooms': [3],
    'characteristics_bathrooms': [2],
    'characteristics_garages': [2],
    'characteristics_area': [170],
    'location_lat': [-17.7675387],
    'location_lng': [-63.11527],
    'extras_Terreno': [480.0],  # Valor ejemplo para el área de terreno,
    'neighborhood_name': le_neighborhood.transform(['Barrio las Pampita']),  # Convertir con LabelEncoder
    'district_name': le_district.transform(['Distrito 6'])  # Convertir con LabelEncoder,
})

# Hacer la predicción
prediccion_precio = xgb_model.predict(casa_nueva)

# Revertir la transformación logarítmica
precio_original = np.exp(prediccion_precio)

# Mostrar los resultados
print(f'El precio logarítmico predicho para la casa es: ${prediccion_precio[0]:.2f}')
print(f'El precio original predicho para la casa es: ${precio_original[0]:.2f}')
