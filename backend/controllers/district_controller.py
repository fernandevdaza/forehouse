import numpy as np
from beanie import PydanticObjectId

from backend.models.district import District, DistrictOutput
from typing import List


class DistrictController:
    def __init__(self):
        pass

    @classmethod
    async def retrieve_districts(cls) -> List[DistrictOutput]:
        districts = await District.find_all().to_list()
        return [DistrictOutput(**district.model_dump()) for district in districts]
