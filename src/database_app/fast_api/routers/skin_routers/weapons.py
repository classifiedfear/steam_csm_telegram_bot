import typing

import fastapi
from pydantic import BaseModel

from src.database_app.database.tables.skin_tables.weapon_table import WeaponTable
from src.database_app.fast_api.dependencies import database
from src.database_app.fast_api.dependencies.common_end_point_executor import weapon_end_point_executor, CommonEndPointExecutor


class WeaponPostModel(BaseModel):
    name: str


weapon_router = fastapi.APIRouter(
    prefix="/weapons",
    tags=["weapons"],
    dependencies=[fastapi.Depends(database.get_db_weapon_context)]
)


@weapon_router.post('/create')
async def create(
        weapon_post_model: WeaponPostModel,
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(weapon_end_point_executor)
):
    return await end_point_executor.create(weapon_post_model)


@weapon_router.get('/id/{id}')
async def get_weapon_by_id(
        id: int,
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(weapon_end_point_executor)
):
    return await end_point_executor.get_by_id(id)


@weapon_router.put('/id/{id}')
async def update_weapon_by_id(
        id: int,
        weapon_post_model: WeaponPostModel,
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(weapon_end_point_executor)
):
    return await end_point_executor.update_by_id(id, weapon_post_model)


@weapon_router.delete('/id/{id}')
async def delete_weapon_by_id(
        id: int,
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(weapon_end_point_executor)
):
    return await end_point_executor.delete_by_id(id)


@weapon_router.get('/name/{name}')
async def get_weapon_by_name(
        name: str,
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(weapon_end_point_executor)
):
    return await end_point_executor.get_by_name(name)


@weapon_router.put('/name/{name}')
async def update_weapon_by_name(
        name: str,
        weapon_post_model: WeaponPostModel,
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(weapon_end_point_executor)
):
    return await end_point_executor.update_by_name(name, weapon_post_model)


@weapon_router.delete('/name/{name}')
async def delete_weapon_by_name(
        name: str,
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(weapon_end_point_executor)
):
    return await end_point_executor.delete_by_name(name)


@weapon_router.post('/create_many')
async def create_many(
        weapon_post_models: typing.List[WeaponPostModel],
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(weapon_end_point_executor)
):
    return await end_point_executor.create_many(weapon_post_models)

@weapon_router.get('/')
async def get_many(weapon_table: WeaponTable = fastapi.Depends(database.get_db_weapon_context)):
    return list(await weapon_table.get_all())


@weapon_router.delete('/id')
async def delete_many_by_id(
        ids: typing.List[int] = fastapi.Query(None),
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(weapon_end_point_executor)
):
    return await end_point_executor.delete_many_by_id(ids)


@weapon_router.delete('/name')
async def delete_many_by_name(
        names: typing.List[str] = fastapi.Query(None),
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(weapon_end_point_executor)
):
    return await end_point_executor.delete_many_by_name(names)


@weapon_router.get('/{name}/skins')
async def get_skins_for_weapon(name: str, weapon_table: WeaponTable = fastapi.Depends(database.get_db_weapon_context)):
    return list(await weapon_table.get_skins_for_weapon(name))


