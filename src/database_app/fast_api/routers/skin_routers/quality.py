import typing

import fastapi
from pydantic import BaseModel

from src.database_app.database.tables.skin_tables.quality_table import QualityTable
from src.database_app.fast_api.dependencies import database
from src.database_app.fast_api.dependencies.common_end_point_executor import CommonEndPointExecutor, quality_end_point_executor

quality_router = fastapi.APIRouter(
    prefix="/qualities",
    tags=["qualities"],
    dependencies=[fastapi.Depends(database.get_db_quality_context)]
)


class Quality(BaseModel):
    name: str


@quality_router.post('/create')
async def create(
        quality: Quality,
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(quality_end_point_executor)
):
    return await end_point_executor.create(quality)


@quality_router.get('/id/{id}')
async def get_weapon_by_id(
        id: int,
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(quality_end_point_executor)
):
    return await end_point_executor.get_by_id(id)


@quality_router.put('/id/{id}')
async def update_weapon_by_id(
        id: int,
        quality: Quality,
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(quality_end_point_executor)
):
    return await end_point_executor.update_by_id(id, quality)


@quality_router.delete('/id/{id}')
async def delete_weapon_by_id(
        id: int,
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(quality_end_point_executor)
):
    return await end_point_executor.delete_by_id(id)


@quality_router.get('/name/{name}')
async def get_weapon_by_name(
        name: str,
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(quality_end_point_executor)
):
    return await end_point_executor.get_by_name(name)


@quality_router.put('/name/{name}')
async def update_weapon_by_name(
        name: str,
        quality: Quality,
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(quality_end_point_executor)
):
    return await end_point_executor.update_by_name(name, quality)


@quality_router.delete('/name/{name}')
async def delete_weapon_by_name(
        name: str,
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(quality_end_point_executor)
):
    return await end_point_executor.delete_by_name(name)


@quality_router.post('/create_many')
async def create_many(
        weapons: typing.List[Quality],
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(quality_end_point_executor)
):
    return await end_point_executor.create_many(weapons)


@quality_router.get('/')
async def get_many(quality_table: QualityTable = fastapi.Depends(database.get_db_quality_context)):
    return list(await quality_table.get_all())


@quality_router.delete('/id')
async def delete_many_by_id(
        ids: typing.List[int] = fastapi.Query(None),
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(quality_end_point_executor)
):
    return await end_point_executor.delete_many_by_id(ids)


@quality_router.delete('/name')
async def delete_many_by_name(
        names: typing.List[str] = fastapi.Query(None),
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(quality_end_point_executor)
):
    return await end_point_executor.delete_many_by_name(names)

