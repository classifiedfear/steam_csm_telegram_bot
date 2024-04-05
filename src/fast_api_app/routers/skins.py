import fastapi
from pydantic import BaseModel

from src.db.tables.skin_table import SkinTable
from src.fast_api_app.dependencies import db

skin_router = fastapi.APIRouter(
    prefix="/skins",
    tags=["skins"],
    dependencies=[fastapi.Depends(db.get_db_skin_table)]
)


class Skin(BaseModel):
    name: str
    stattrak_existence: bool = False


@skin_router.post("/")
async def create(skin: Skin, skin_table: SkinTable = fastapi.Depends(db.get_db_skin_table)):
    skin_dict = skin.model_dump()
    id = await skin_table.create(**skin_dict)
    skin_dict['id'] = id
    return skin_dict


@skin_router.get("/id/{id}")
async def get_skin_by_id(id: int, skin_table: SkinTable = fastapi.Depends(db.get_db_skin_table)):
    return await skin_table.get(id)


@skin_router.put("/id/{id}")
async def update_skin_by_id(id: int, skin: Skin, skin_table: SkinTable = fastapi.Depends(db.get_db_skin_table)):
    await skin_table.update(id, **skin.model_dump())


@skin_router.delete("/id/{id}")
async def delete_skin_by_id(id: int, skin_table: SkinTable = fastapi.Depends(db.get_db_skin_table)):
    await skin_table.delete(id)
    return {'success': True}


@skin_router.get('/name/{name}')
async def get_skin_by_name(name: str, skin_table: SkinTable = fastapi.Depends(db.get_db_skin_table)):
    return await skin_table.get_by_name(name)


@skin_router.put('/name/{name')
async def update_skin_by_name(name: str, skin: Skin, skin_table: SkinTable = fastapi.Depends(db.get_db_skin_table)):
    await skin_table.update_by_name(name, **skin.model_dump())


@skin_router.delete('/name/{name}')
async def delete_skin_by_name(name: str, skin_table: SkinTable = fastapi.Depends(db.get_db_skin_table)):
    await skin_table.delete_by_name(name)
    return {'success': True}


@skin_router.get('/')
async def get_skins(skin_table: SkinTable = fastapi.Depends(db.get_db_skin_table)):
    result = await skin_table.get_skins()
    return list(result)