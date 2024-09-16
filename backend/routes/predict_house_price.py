from fastapi import APIRouter, HTTPException, Depends
from backend.controllers.house_controller import HouseController
from backend.models.house import HouseInput, HouseOutput
from typing import List
import logging
import xgboost as xgb

router = APIRouter(prefix='/predict_house_price', tags=['Predict House Price'])

logger = logging.getLogger(__name__)


@router.post("/predict_one", response_model=HouseOutput)
async def predict_price_one(house: HouseInput):
    """Predict the price of a single house."""
    try:
        house_output = await HouseController().predict_price(house)
        return house_output
    except ValueError as e:
        logger.error(f"Error de validación: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except xgb.core.XGBoostError as e:
        logger.error(f"Error en el modelo de predicción: {e}")
        raise HTTPException(status_code=500, detail="Error en el modelo de predicción.")
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        raise HTTPException(status_code=500, detail="Ocurrió un error al predecir el precio de la casa.")


@router.post("/predict_many", response_model=List[HouseOutput])
async def predict_price_many(houses: List[HouseInput]):
    """Predict the price of multiple houses."""
    predictions = []
    try:
        for house in houses:
            house_output = await HouseController().predict_price(house)
            predictions.append(house_output)

        return predictions
    except ValueError as e:
        logger.error(f"Error de validación en una de las casas: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except xgb.core.XGBoostError as e:
        logger.error(f"Error en el modelo de predicción: {e}")
        raise HTTPException(status_code=500, detail="Error en el modelo de predicción.")
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        raise HTTPException(status_code=500, detail="Ocurrió un error al predecir el precio de las casas.")


@router.get("/get_all_predicted_houses", response_model=List[HouseOutput])
async def get_all_predicted_houses():
    """Get all the predictions."""
    try:
        predictions = await HouseController().get_all_predictions()
        return predictions
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        raise HTTPException(status_code=500, detail="Ocurrió un error al obtener las predicciones.")
