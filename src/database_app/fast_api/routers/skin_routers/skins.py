import typing

import fastapi
from pydantic import BaseModel

from src.database_app.database.tables.skin_tables.skin_table import SkinTable
from src.database_app.fast_api.dependencies import database
from src.database_app.fast_api.dependencies.common_end_point_executor import skin_end_point_executor , CommonEndPointExecutor

skin_router = fastapi.APIRouter(
    prefix="/skins",
    tags=["skins"])


class SkinPostModel(BaseModel):
    name: str
    stattrak_existence: bool = False


@skin_router.post("/create")
async def create(
        skin_post_model: SkinPostModel,
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(skin_end_point_executor)
):
    return await end_point_executor.create(skin_post_model)


@skin_router.get("/id/{id}")
async def get_skin_by_id(
        id: int,
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(skin_end_point_executor)
):
    return await end_point_executor.get_by_id(id)


@skin_router.put("/id/{id}")
async def update_skin_by_id(
        id: int, skin_post_model: SkinPostModel,
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(skin_end_point_executor)
):
    return await end_point_executor.update_by_id(id, skin_post_model)


@skin_router.delete("/id/{id}")
async def delete_skin_by_id(
        id: int,
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(skin_end_point_executor)
):
    return await end_point_executor.delete_by_id(id)


@skin_router.get('/name/{name}')
async def get_skin_by_name(
        name: str,
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(skin_end_point_executor)
):
    return await end_point_executor.get_by_name(name)


@skin_router.put('/name/{name')
async def update_skin_by_name(
        name: str,
        skin_post_model: SkinPostModel,
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(skin_end_point_executor)
):
    return await end_point_executor.update_by_name(name, skin_post_model)


@skin_router.delete('/name/{name}')
async def delete_skin_by_name(
        name: str,
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(skin_end_point_executor)
):
    return await end_point_executor.delete_by_name(name)


@skin_router.post('/create_many')
async def create_many(
        skins: typing.List[SkinPostModel],
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(skin_end_point_executor)
):
    return await end_point_executor.create_many(skins)


@skin_router.get('/')
async def get_many(skin_table: SkinTable = fastapi.Depends(database.get_db_skin_context)):
    return list(await skin_table.get_all())


@skin_router.delete('/id')
async def delete_many_by_id(
        ids: typing.List[int] = fastapi.Query(None),
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(skin_end_point_executor)
):
    return await end_point_executor.delete_many_by_id(ids)


@skin_router.delete('/name')
async def delete_many_by_name(
        names: typing.List[str] = fastapi.Query(None),
        end_point_executor: CommonEndPointExecutor = fastapi.Depends(skin_end_point_executor)
):
    return await end_point_executor.delete_many_by_name(names)
