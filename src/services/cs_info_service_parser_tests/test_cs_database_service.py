import pytest
import pytest_unordered

from src.services.cs_skins_data_retriever.cs_skin_data_retriever import CsInfoService
from src.services.misc.common_request_executor import CommonRequestExecutor


QUALITIES_PARAMETRIZE = (
    ('weapon', 'skin', 'expected'),
    [
        ('AK-47', 'Asiimov', ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred']),
        ('AWP', 'Asiimov', ['Field-Tested', 'Well-Worn', 'Battle-Scarred']),
        ('Desert Eagle', 'Code Red', ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred']),
        ('USP-S', 'Cortex', ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred']),
        ('★ Karambit', 'Black Laminate', ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred'])
    ]
)

STATTRAK_PARAMETRIZE = (
    ('weapon', 'skin', 'expected'),
    [
        ('AK-47', 'Asiimov', True),
        ('R8 Revolver', 'Inlay', False),
        ('Desert Eagle', 'Code Red', True),
        ('USP-S', 'Cortex', True),
        ('P90', 'Asiimov', True)
    ]
)

KNIFE_PARAMETRIZE = (
    ('knife', 'expected'),
    [
        ('★ Ursus Knife', ['Damascus Steel', 'Doppler', 'Fade']),
        ('★ Karambit', ['Doppler', 'Fade', 'Forest DDPAT'])

    ]
)

SKINS_PARAMETRIZE = (
    ('skin', 'expected'),
    [
        ('AK-47', ['Red Laminate', 'Redline', 'Point Disarray']),
        ('R8 Revolver', ['Grip', 'Memento', 'Bone Forged']),
        ('★ Karambit', ['Black Laminate'])
    ]
)


@pytest.fixture
def retriever() -> CsInfoService:
    common_request_executor = CommonRequestExecutor()
    service = CsInfoService(common_request_executor)
    return service


@pytest.mark.asyncio
async def test_should_get_all_existence_weapons(retriever):
    result = await retriever.get_weapons()
    for weapon in ['AK-47', 'AWP', 'R8 Revolver', 'USP-S']:
        assert weapon in result


@pytest.mark.parametrize(*SKINS_PARAMETRIZE)
@pytest.mark.asyncio
async def test_should_get_all_existence_skins_for_weapon(retriever, skin, expected):
    result = await retriever.get_skins_for_weapon(skin)
    for expected_skin in expected:
        assert expected_skin in result


@pytest.mark.parametrize(*KNIFE_PARAMETRIZE)
@pytest.mark.asyncio
async def test_should_get_all_existence_skins_for_knife(retriever, knife, expected):
    result = await retriever.get_skins_for_weapon(knife)
    for expected_knife in expected:
        assert expected_knife in result


@pytest.mark.parametrize(*QUALITIES_PARAMETRIZE)
@pytest.mark.asyncio
async def test_should_get_qualities_for_weapon_and_skin(retriever, weapon, skin, expected):
    result = await retriever.get_qualities_for_weapon_and_skin(weapon, skin)
    assert expected == pytest_unordered.unordered(result)


@pytest.mark.parametrize(*STATTRAK_PARAMETRIZE)
@pytest.mark.asyncio
async def test_should_get_stattrak_existence(retriever, weapon, skin, expected):
    result = await retriever.get_stattrak_existence_for_weapon_and_skin(weapon, skin)
    assert expected == result

