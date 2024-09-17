import numpy as np
from beanie import PydanticObjectId
from fastapi import HTTPException

from backend.models.neighborhood import Neighborhood, NeighborhoodOutput
from typing import List


class NeighborhoodController:
    def __init__(self):
        pass

    @classmethod
    async def retrieve_neighborhoods(cls) -> List[NeighborhoodOutput]:
        neighborhoods = await Neighborhood.find_all().to_list()
        return [NeighborhoodOutput(**neighborhood.model_dump()) for neighborhood in neighborhoods]

    @classmethod
    async def get_neighborhood_price_per_m2(cls, neighborhood_id: PydanticObjectId) -> float:
        neighborhood = await Neighborhood.get(neighborhood_id)
        if neighborhood is None:
            raise ValueError(f"Neighborhood with id {neighborhood_id} not found.")
        return neighborhood.price_per_m2

    @classmethod
    async def neighborhood_add_price_per_m2(cls, neighborhood_name: str, price_per_m2: float):
        """Agregar precio por m2 a un vecindario"""
        try:
            neighborhood = await Neighborhood.find_by_name(neighborhood_name)
            if price_per_m2 < 0:
                raise ValueError("El precio por m² no puede ser negativo.")

            if neighborhood is None:
                raise LookupError(f"Neighborhood with name {neighborhood_name} not found.")

            neighborhood.price_per_m2 = price_per_m2
            await neighborhood.save()

            return
        except LookupError:
            raise
        except ValueError:
            raise
        except Exception as e:
            raise RuntimeError(f"Ocurrió un error al guardar el vecindario: {e}") from e

    @classmethod
    async def get_neighborhood_by_id(cls, neighborhood_id: PydanticObjectId) -> NeighborhoodOutput:
        neighborhood = await Neighborhood.get(neighborhood_id)
        if neighborhood is None:
            raise HTTPException(status_code=404, detail=f"Neighborhood with id {neighborhood_id} not found.")
        return NeighborhoodOutput(**neighborhood.model_dump())
