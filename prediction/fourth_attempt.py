import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder, StandardScaler
import numpy as np

# Cargar los datos
df = pd.read_csv('prediction/dataset_ready_to_go3.csv')

# Aplicar la transformación logarítmica al precio
df['log_price'] = np.log(df['price'])

# Crear nuevas características
df['area_terreno_ratio'] = df['characteristics_area'] / df['extras_Terreno']
df['bedrooms_per_area'] = df['characteristics_bedrooms'] / df['characteristics_area']

# Seleccionar las columnas para el modelo, eliminando neighborhood_name y district_name
features = ['characteristics_bedrooms', 'characteristics_bathrooms', 'characteristics_garages',
            'characteristics_area', 'location_lat', 'location_lng', 'extras_Terreno',
            'area_terreno_ratio', 'bedrooms_per_area']

# Definir X (características) e y (precio logarítmico)
X = df[features]
y = df['log_price']

# Escalar las características
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Convertir los datos de entrenamiento y prueba a DMatrix con GPU activado
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# Definir los hiperparámetros ajustados
param = {
    'objective': 'reg:squarederror',
    'max_depth': 4,  # Reducción de la profundidad del árbol para evitar overfitting
    'learning_rate': 0.05,  # Tasa de aprendizaje más baja para un ajuste más preciso
    'colsample_bytree': 0.7,  # Reducción de la muestra de columnas
    'subsample': 0.7,  # Uso de una muestra más pequeña de datos
    'n_estimators': 100,  # Aumento del número de estimadores para mejorar el ajuste
    'tree_method': 'gpu_hist',  # Usar la GPU
    'device': 'cuda'
}

# Entrenar el modelo usando la GPU
model = xgb.train(param, dtrain, num_boost_round=150, evals=[(dtest, "Test")])

# Hacer predicciones en los datos de prueba
y_pred = model.predict(dtest)
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
print(f'Error cuadrático medio (MSE): {mse}')
print(f'Raíz del error cuadrático medio (RMSE): {rmse}')

# Predecir con un nuevo ejemplo
casa_nueva = pd.DataFrame({
    'characteristics_bedrooms': [3],
    'characteristics_bathrooms': [2],
    'characteristics_garages': [2],
    'characteristics_area': [170],
    'location_lat': [-17.7675387],
    'location_lng': [-63.11527],
    'extras_Terreno': [480.0],
    'area_terreno_ratio': [170 / 480.0],
    'bedrooms_per_area': [3 / 170]
})

# Escalar la nueva entrada y convertirla a DMatrix
casa_nueva_scaled = scaler.transform(casa_nueva)
dnew = xgb.DMatrix(casa_nueva_scaled)

# Hacer la predicción con el nuevo modelo
prediccion_precio = model.predict(dnew)

# Revertir la transformación logarítmica
precio_original = np.exp(prediccion_precio)
print(f'El precio original predicho para la casa es: ${precio_original[0]:.2f}')
