from fastapi import APIRouter, Body, HTTPException, Response
from typing import List
from backend.controllers.neighborhood_controller import NeighborhoodController
from backend.models.neighborhood import NeighborhoodOutput
from backend.models.district import DistrictOutput, DistrictAndNeighborhood
from backend.controllers.district_controller import DistrictController
from backend.utils.build_district_object import build_district_object
from backend.models.neighborhood import Neighborhood, NeighborhoodPriceM2

router = APIRouter(prefix='/data', tags=['Neighborhoods'])

embed = Body(..., embed=True)


@router.get("", response_model=List[DistrictAndNeighborhood])
async def get_data():
    """Retrieve all neighborhoods"""
    neighborhoods = await NeighborhoodController.retrieve_neighborhoods()
    districts = await DistrictController.retrieve_districts()

    return build_district_object(districts, neighborhoods)


@router.post("/add_price_per_m2_to_neighborhood", responses={200: {"description": "Neighborhoods updated"}})
async def neighborhood_add_price_per_m2(neighborhoods: List[NeighborhoodPriceM2]):
    """Add or update the price per m2 to the neighborhoods"""
    try:
        for neighborhood in neighborhoods:
            await NeighborhoodController.neighborhood_add_price_per_m2(
                neighborhood.neighborhood_name, neighborhood.price_per_m2)

        return Response(status_code=200, content="Vecindarios actualizados.")
    except LookupError as e:
        return Response(status_code=404, content=str(e))
    except ValueError as e:
        return Response(status_code=400, content=str(e))
    except Exception as e:
        return Response(status_code=500, content=str(e))


