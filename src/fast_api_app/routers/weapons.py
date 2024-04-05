import fastapi
from pydantic import BaseModel

from ..dependencies import db
from ...db.tables.weapon_table import WeaponTable


class Weapon(BaseModel):
    name: str


weapon_router = fastapi.APIRouter(
    prefix="/weapons",
    tags=["weapons"],
    dependencies=[fastapi.Depends(db.get_db_weapon_table)]
)


@weapon_router.post('/')
async def create(weapon: Weapon, weapon_table: WeaponTable = fastapi.Depends(db.get_db_weapon_table)):
    weapon_dict = weapon.model_dump()
    id = await weapon_table.create(**weapon.model_dump())
    weapon_dict['id'] = id
    return weapon_dict


@weapon_router.get('/id/{id}')
async def get_weapon_by_id(id: int, weapon_table: WeaponTable = fastapi.Depends(db.get_db_weapon_table)):
    if result := await weapon_table.get(id):
        return result
    else:
        return {"message": "Not found"}


@weapon_router.put('/id/{id}')
async def update_weapon_by_id(
        id: int, weapon: Weapon, weapon_table: WeaponTable = fastapi.Depends(db.get_db_weapon_table)
):
    await weapon_table.update(id, **weapon.model_dump())
    return {'message': 'updated'}


@weapon_router.delete('/id/{id}')
async def delete_weapon_by_id(id: int, weapon_table: WeaponTable = fastapi.Depends(db.get_db_weapon_table)):
    await weapon_table.delete(id)
    return {'message': 'deleted'}


@weapon_router.get('/name/{name}')
async def get_weapon_by_name(name: str, weapon_table: WeaponTable = fastapi.Depends(db.get_db_weapon_table)):
    if result := await weapon_table.get_by_name(name):
        return result
    else:
        return {"message": "Not found"}


@weapon_router.put('/name/{name}')
async def update_weapon_by_name(
        name: str, weapon: Weapon, weapon_table: WeaponTable = fastapi.Depends(db.get_db_weapon_table)
):
    await weapon_table.update_by_name(name, **weapon.model_dump())
    return {'message': 'updated'}


@weapon_router.delete('/name/{name}')
async def delete_weapon_by_name(name: str, weapon_table: WeaponTable = fastapi.Depends(db.get_db_weapon_table)):
    await weapon_table.delete_by_name(name)
    return {'message': 'deleted'}


@weapon_router.get('/')
async def get_many(weapon_table: WeaponTable = fastapi.Depends(db.get_db_weapon_table)):
    result = await weapon_table.get_weapons()
    return list(result)


@weapon_router.get('/{name}/skins')
async def get_skins_for_weapon(name: str, weapon_table: WeaponTable = fastapi.Depends(db.get_db_weapon_table)):
    result = await weapon_table.get_skins_for_weapon(name)
    return list(result)


