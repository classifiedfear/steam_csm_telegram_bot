import asyncio
import os

import pytest
import pytest_asyncio
from sqlalchemy import URL

from src.db import TGQueries
from src.db import BotDatabase, Base
from src.db import DatabaseSkinFiller


@pytest.fixture(scope="module")
def event_loop(request):
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
def get_db_url():
    url = URL.create(
        'postgresql+asyncpg',
        username=os.getenv('db_user'),
        password=os.getenv('db_password'),
        port=os.getenv('db_port'),
        host=os.getenv('db_host')
    )
    return url


@pytest_asyncio.fixture(scope="module", autouse=True)
async def db(event_loop, get_db_url):
    db = BotDatabase(get_db_url)
    await db.proceed_schemas(Base.metadata)
    yield db
    await db.drop_all_tables(Base.metadata)


@pytest.mark.parametrize(
    'skin_name', ['Asiimov', 'Code Red', 'Cortex']
)
@pytest.mark.asyncio
async def test_should_add_skin(db, skin_name):
    id = await DatabaseSkinFiller.add_skin(db.get_session_maker(), skin_name)
    result = await DatabaseSkinFiller.get_skin(db.get_session_maker(), id)
    assert result.name == skin_name


@pytest.mark.parametrize(
    ['skin_name', 'stattrak_existence'],
    [('Hyper Beast', 2), ('Phantom Disruptor', 1), ('Temukau', 0)]
)
@pytest.mark.asyncio
async def test_should_add_skin_with_different_stattraks_existence(db, skin_name, stattrak_existence):
    id = await DatabaseSkinFiller.add_skin(db.get_session_maker(), skin_name, stattrak_existence)
    result = await DatabaseSkinFiller.get_skin(db.get_session_maker(), id)
    assert result.name == skin_name


@pytest.mark.parametrize(
    'weapon_name', ['AK-47', 'Desert Eagle', 'AWP']
)
@pytest.mark.asyncio
async def test_should_add_weapon(db, weapon_name):
    id = await DatabaseSkinFiller.add_weapon(db.get_session_maker(), weapon_name)
    result = await DatabaseSkinFiller.get_weapon(db.get_session_maker(), id)
    assert result.name == weapon_name


@pytest.mark.parametrize(
    'quality_title', ['Minimal Wear', 'Well-Worn', 'Battle-Scarred']
)
@pytest.mark.asyncio
async def test_should_add_quality(db, quality_title):
    id = await DatabaseSkinFiller.add_quality(db.get_session_maker(), quality_title)
    result = await DatabaseSkinFiller.get_quality(db.get_session_maker(), id)
    assert result.title == quality_title


@pytest.mark.parametrize(
    ['skin_name', 'weapon_name', 'quality_title', 'stattrak_existence'],
    [
        ('Block-18', 'Glock-18', 'Field-Tested', 2), ('Analog Input', 'Sawed-Off', 'Factory New', 1)
    ]
)
@pytest.mark.asyncio
async def test_should_add_associations_wsq(db, skin_name, weapon_name, quality_title, stattrak_existence):
    skin_id = await DatabaseSkinFiller.add_skin(db.get_session_maker(), skin_name, stattrak_existence)
    weapon_id = await DatabaseSkinFiller.add_weapon(db.get_session_maker(), weapon_name)
    quality_id = await DatabaseSkinFiller.add_quality(db.get_session_maker(), quality_title)
    await DatabaseSkinFiller.add_associations_between_weapon_skin_quality(
        db.get_session_maker(), weapon_id, skin_id, quality_id
    )
    result = await DatabaseSkinFiller.get_skin_associations(db.get_session_maker(), skin_id, weapon_id, quality_id)
    assert result == (skin_name, weapon_name, quality_title, stattrak_existence)


@pytest.mark.asyncio
async def test_should_get_random_skin(db):
    result = await TGQueries.get_random_weapon_from_db(db.get_session_maker())
    assert result in [('Block-18', 'Glock-18', 'Field-Tested', 2), ('Analog Input', 'Sawed-Off', 'Factory New', 1)]


@pytest.mark.asyncio
async def test_should_get_skins_for_weapon(db):
    weapon_id = await DatabaseSkinFiller.get_weapon_id_by_name(db.get_session_maker(), 'Glock-18')
    result = await TGQueries.get_skins_for_weapon(db.get_session_maker(), weapon_id)
    assert result == [('Block-18',)]