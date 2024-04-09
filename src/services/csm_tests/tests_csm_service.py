from typing import List

import pytest



from src.misc.link_tools import Pager
from src.services.csm.csm_market_skin_data_retriever import CsmMarketSkinDataRetriever
from src.services.csm.exceptions import RequestException
from src.services.csm.resources.dto import CsmSkinResponseDTO
from src.services.misc.dto import SkinRequestDTO


@pytest.fixture
def ak_47_skin_dto():
    return SkinRequestDTO(
        'AK-47', 'Asiimov', 'Battle-Scarred', False
    )


@pytest.fixture
def service() -> CsmMarketSkinDataRetriever:
    service = CsmMarketSkinDataRetriever()
    return service


@pytest.mark.asyncio
async def test_should_get_csm_list_skin_data_dto(ak_47_skin_dto, service):
    result = await service.get_market_skins(ak_47_skin_dto)
    _should_equal_tuple_with_csm_skin_dtos(result)


@pytest.mark.asyncio
async def test_should_get_csm_skin_dto_list_from_all_pages(ak_47_skin_dto, service):
    pager = Pager(60)
    while True:
        try:
            response = await service.get_market_skins(
                ak_47_skin_dto, offset=pager.get_next_offset()
            )
            _should_equal_tuple_with_csm_skin_dtos(response)
        except RequestException:
            break


def _should_equal_tuple_with_csm_skin_dtos(result: List[CsmSkinResponseDTO]):
    assert result
    for skin_dto in result:
        assert skin_dto.name == 'AK-47 | Asiimov (Battle-Scarred)'
        assert isinstance(skin_dto.skin_float, float)
        assert isinstance(skin_dto.price, float)
        assert isinstance(skin_dto.overpay_float, float)

