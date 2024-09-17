import numpy as np
import xgboost as xgb
from beanie import PydanticObjectId
from backend.models.house import House, HouseInput, HouseOutput, Prices
from backend.controllers.neighborhood_controller import NeighborhoodController
import pandas as pd
from typing import Tuple, Optional, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HouseController:
    def __init__(self):
        try:
            self.with_price_model = xgb.XGBRegressor()
            self.without_price_model = xgb.XGBRegressor()
            self.with_price_model.load_model('xgboost_models/with_price_model.bst')
            self.without_price_model.load_model('xgboost_models/without_price_model.bst')
            logger.info("Modelos cargados exitosamente.")
        except FileNotFoundError as e:
            logger.error(f"Archivo de modelo no encontrado: {e}")
            raise
        except xgb.core.XGBoostError as e:
            logger.error(f"Error al cargar el modelo de XGBoost: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado al inicializar HouseController: {e}")
            raise

    async def predict_price(self, house: HouseInput) -> HouseOutput:
        """Predict the price of a house."""
        try:
            features_price, features_no_price = await self._preprocess_features(house)

            house_to_predict_with_price = pd.DataFrame(features_price)
            house_to_predict_no_price = pd.DataFrame(features_no_price)

            price_model_prediction = round(np.exp(self.with_price_model.predict(house_to_predict_with_price)[0]), 2)
            no_price_model_prediction = round(np.exp(self.without_price_model.predict(house_to_predict_no_price)[0]), 2)
            final_predicted_price = (price_model_prediction + no_price_model_prediction) / 2

            prices = Prices(
                from_price_model=price_model_prediction,
                from_no_price_model=no_price_model_prediction,
                final_predicted_price=final_predicted_price
            )

            house_to_save = House(
                bedrooms=house.bedrooms,
                bathrooms=house.bathrooms,
                garages=house.garages,
                built_area=house.built_area,
                terrain_area=house.terrain_area,
                lat=house.lat,
                lng=house.lng,
                neighborhood_id=house.neighborhood_id,
                district_id=house.district_id,
                prices=prices
            )
            inserted_house = await house_to_save.create()

            house_output = HouseOutput(
                _id=inserted_house.id,
                bedrooms=house.bedrooms,
                bathrooms=house.bathrooms,
                garages=house.garages,
                built_area=house.built_area,
                terrain_area=house.terrain_area,
                lat=house.lat,
                lng=house.lng,
                neighborhood_id=house.neighborhood_id,
                district_id=house.district_id,
                prices=prices
            )

            logger.info(f"Predicción realizada exitosamente para la casa con ID: {inserted_house.id}")
            return house_output

        except xgb.core.XGBoostError as e:
            logger.error(f"Error durante la predicción con XGBoost: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado en predict_price: {e}")
            raise

    @classmethod
    async def _preprocess_features(cls, house: HouseInput) -> Tuple[dict, dict]:
        """Preprocesar las características de la casa para la predicción."""
        try:
            if not (house.bedrooms >= 0 and
                    house.bathrooms >= 0 and
                    house.garages >= 0 and
                    house.built_area >= 0 and
                    house.terrain_area >= 0):
                raise ValueError("Las características numéricas no pueden ser negativas.")

            neighborhood = await NeighborhoodController.get_neighborhood_by_id(house.neighborhood_id)

            house.lat = neighborhood.geometry.coordinates[1]
            house.lng = neighborhood.geometry.coordinates[0]

            # if not (-90 <= house.lat <= 90):
            #     raise ValueError("La latitud debe estar entre -90 y 90 grados.")
            #
            # if not (-180 <= house.lng <= 180):
            #     raise ValueError("La longitud debe estar entre -180 y 180 grados.")

            if house.neighborhood_id is None or house.district_id is None:
                raise ValueError("Los IDs de vecindario y distrito no pueden ser nulos.")

            if not isinstance(house.neighborhood_id, PydanticObjectId) or not isinstance(house.district_id,
                                                                                         PydanticObjectId):
                raise TypeError("Los IDs de vecindario y distrito deben ser de tipo PydanticObjectId.")

        except (ValueError, TypeError) as e:
            logger.error(f"Error en la validación de características: {e}")
            raise

        try:
            price_per_m2 = await NeighborhoodController.get_neighborhood_price_per_m2(str(house.neighborhood_id))
            if price_per_m2 is None:
                raise ValueError(f"No se pudo obtener el precio por m² para el vecindario ID: {house.neighborhood_id}")

        except Exception as e:
            logger.error(f"Error al obtener el precio por m² del vecindario: {e}")
            raise

        features_price = {
            "characteristics_bedrooms": [house.bedrooms],
            "characteristics_bathrooms": [house.bathrooms],
            "characteristics_garages": [house.garages],
            "characteristics_area": [house.built_area],
            "location_lat": [house.lat],
            "location_lng": [house.lng],
            "extras_Terreno": [house.terrain_area],
            "price_per_m2": [price_per_m2]
        }
        features_no_price = {
            "characteristics_bedrooms": [house.bedrooms],
            "characteristics_bathrooms": [house.bathrooms],
            "characteristics_garages": [house.garages],
            "characteristics_area": [house.built_area],
            "location_lat": [house.lat],
            "location_lng": [house.lng],
            "extras_Terreno": [house.terrain_area]
        }
        return features_price, features_no_price

    @classmethod
    async def get_all_predictions(cls) -> List[HouseOutput]:
        """Get all the predictions."""
        try:
            houses = await House.all().to_list()
            #Añadir Nombre de barrio y precio por m2
            predictions = []
            for house in houses:
                neighborhood = await NeighborhoodController.get_neighborhood_by_id(house.neighborhood_id)
                predictions.append(HouseOutput(
                    _id=house.id,
                    bedrooms=house.bedrooms,
                    bathrooms=house.bathrooms,
                    garages=house.garages,
                    built_area=house.built_area,
                    terrain_area=house.terrain_area,
                    lat=house.lat,
                    lng=house.lng,
                    neighborhood_id=house.neighborhood_id,
                    district_id=house.district_id,
                    prices=house.prices,
                    neighborhood_name=neighborhood.nombre,
                    price_per_m2=neighborhood.price_per_m2
                ))

            return predictions
        except Exception as e:
            logger.error(f"Error inesperado en get_all_predictions: {e}")
            raise
