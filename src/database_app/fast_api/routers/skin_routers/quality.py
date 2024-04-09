import fastapi
from pydantic import BaseModel

from src.database_app.database.tables.skin_tables.quality_table import QualityTable
from src.database_app.fast_api.dependencies import database

quality_router = fastapi.APIRouter(
    prefix="/qualities",
    tags=["qualities"],
    dependencies=[fastapi.Depends(database.get_db_quality_table)]
)


class Quality(BaseModel):
    name: str


@quality_router.post('/')
async def create(quality: Quality, quality_table: QualityTable = fastapi.Depends(database.get_db_quality_table)):
    quality_dict = quality.model_dump()
    id = await quality_table.create(**quality_dict)
    quality_dict['id'] = id
    return quality_dict


@quality_router.get('/id/{id}')
async def get_by_id(id: int, quality_table: QualityTable = fastapi.Depends(database.get_db_quality_table)):
    return await quality_table.get(id)


@quality_router.put('/id/{id}')
async def update_by_id(
        id: int, quality: Quality, quality_table: QualityTable = fastapi.Depends(database.get_db_quality_table)
):
    await quality_table.update(id, **quality.model_dump())


@quality_router.delete('/id/{id}')
async def delete_by_id(id: int, quality_table: QualityTable = fastapi.Depends(database.get_db_quality_table)):
    await quality_table.delete(id)


@quality_router.get('/name/{name}')
async def get_by_name(name: str, quality_table: QualityTable = fastapi.Depends(database.get_db_quality_table)):
    return await quality_table.get_by_name(name)


@quality_router.put('/name/{name}')
async def update_by_name(
        name: str, quality: Quality, quality_table: QualityTable = fastapi.Depends(database.get_db_quality_table)
):
    await quality_table.update_by_name(name, **quality.model_dump())


@quality_router.delete('/name/{name}')
async def delete_by_name(name: str, quality_table: QualityTable = fastapi.Depends(database.get_db_quality_table)):
    await quality_table.delete_by_name(name)

@quality_router.get('/')
async def get_all(quality_table: QualityTable = fastapi.Depends(database.get_db_quality_table)):
    return list(await quality_table.get_all())