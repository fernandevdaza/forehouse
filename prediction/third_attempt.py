import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

# Cargar los datos
df = pd.read_csv('prediction/dataset_ready_to_go3.csv')

# Aplicar la transformación logarítmica al precio
df['log_price'] = np.log(df['price'])

# Seleccionar las columnas para el modelo
features = ['characteristics_bedrooms', 'characteristics_bathrooms', 'characteristics_garages',
            'characteristics_area', 'location_lat', 'location_lng', 'extras_Terreno',
            'neighborhood_name', 'district_name']

# Aplicar Label Encoding a las columnas categóricas
from sklearn.preprocessing import LabelEncoder
le_neighborhood = LabelEncoder()
le_district = LabelEncoder()

df['neighborhood_name'] = le_neighborhood.fit_transform(df['neighborhood_name'])
df['district_name'] = le_district.fit_transform(df['district_name'])

# Definir X (características) e y (precio logarítmico)
X = df[features]
y = df['log_price']

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear el modelo XGBoost
xgb_model = XGBRegressor()

# Definir el espacio de búsqueda de hiperparámetros
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.3],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0]
}

# Utilizar GridSearchCV para buscar los mejores hiperparámetros
grid_search = GridSearchCV(xgb_model, param_grid, cv=5, scoring='neg_mean_squared_error', verbose=1)
grid_search.fit(X_train, y_train)

# Mejor estimador y sus parámetros
best_xgb_model = grid_search.best_estimator_
print(f"Mejores hiperparámetros: {grid_search.best_params_}")

# Evaluación con el mejor modelo
y_pred = best_xgb_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5

print(f'Error cuadrático medio (MSE) después de ajustar hiperparámetros: {mse}')
print(f'Raíz del error cuadrático medio (RMSE) después de ajustar hiperparámetros: {rmse}')

# Validación cruzada con el mejor modelo
cv_scores = cross_val_score(best_xgb_model, X, y, cv=5, scoring='neg_mean_squared_error')
cv_rmse_scores = np.sqrt(-cv_scores)
print(f'RMSE medio en validación cruzada: {cv_rmse_scores.mean()}')


casa_nueva = pd.DataFrame({
    'characteristics_bedrooms': [3],
    'characteristics_bathrooms': [2],
    'characteristics_garages': [2],
    'characteristics_area': [170],
    'location_lat': [-17.7675387],
    'location_lng': [-63.11527],
    'extras_Terreno': [480.0],  # Valor ejemplo para el área de terreno
    'neighborhood_name': le_neighborhood.transform(['Barrio las Pampita']),  # Convertir con LabelEncoder
    'district_name': le_district.transform(['Distrito 6'])  # Convertir con LabelEncoder
})


prediccion_precio = best_xgb_model.predict(casa_nueva)

# Revertir la transformación logarítmica
precio_original = np.exp(prediccion_precio)
print(f'El precio original predicho para la casa es: ${precio_original[0]:.2f}')