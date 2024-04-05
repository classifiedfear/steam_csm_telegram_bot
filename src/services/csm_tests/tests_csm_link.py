import pytest

from src.services.csm.links.csm_market_skin_asset_id_link import CsmMarketSkinAssetIdLink
from src.services.csm.links.csm_market_skin_data_link import CsmMarketSkinDataLink
from src.misc.constants import tests_const
from src.misc.dto import SkinRequestDTO


@pytest.mark.parametrize(
    ('skin_dto', 'result'),
    (
        (SkinRequestDTO('AK-47', 'Asiimov', 'Field-Tested', False), tests_const.RESULT_CSM_AK_47_LINK),
        (SkinRequestDTO('Desert Eagle', 'Code Red', 'Battle-Scarred', True), tests_const.RESULT_CSM_DESERT_EAGLE_LINK),
    )
)
def test_should_create_link_for_csm(skin_dto, result):
    link = CsmMarketSkinAssetIdLink.create(skin_dto)
    assert link == result


def test_should_change_offset_in_link():
    link = CsmMarketSkinAssetIdLink.create(SkinRequestDTO('AK-47', 'Asiimov', 'Field-Tested', False))
    first_offset_result = link.find('offset=0')
    link = CsmMarketSkinAssetIdLink.create(SkinRequestDTO('AK-47', 'Asiimov', 'Field-Tested', False), offset=60)
    second_offset_result = link.find('offset=60')

    assert first_offset_result != -1
    assert second_offset_result != -1


def test_should_create_link_for_current_skin():
    link = CsmMarketSkinDataLink.create()
    assert link == tests_const.RESULT_CSM_SPECIFIC_SKIN_LINK

