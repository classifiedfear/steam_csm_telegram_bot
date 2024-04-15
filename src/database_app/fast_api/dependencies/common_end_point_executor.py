import typing

import fastapi

from sqlalchemy.exc import IntegrityError

from src.database_app.database.tables.abc_table.table import Table
from src.database_app.fast_api.dependencies import database


class CommonEndPointExecutor:
    def __init__(self, context: Table):
        self._context = context

    async def create(self, post_model):
        try:
            db_model = await self._context.create(post_model.model_dump())
        except IntegrityError:
            return {"success": False, "message": f"Item with this name already exists, names need to be unique!"}
        await self._context.save_changes()
        return db_model

    async def get_by_id(self, id: int):
        if db_model := await self._context.get_by_id(id):
            return db_model
        else:
            return {"status": False, "message": f"Item with id - {str(id)!r} does not exist!"}

    async def update_by_id(self, id: int, put_data):
        try:
            db_model = await self._context.update_by_id(id, **put_data.model_dump())
        except IntegrityError:
            return {"success": False, "message": "Item with this name already exists, names need be unique!"}
        if db_model is None:
            return {"status": False, "message": f"Item with id - {str(id)!r} does not exist!"}
        await self._context.save_changes()
        return db_model

    async def delete_by_id(self, id: int):
        if await self._context.delete_by_id(id):
            await self._context.save_changes()
            return {'success': True, "message": f"Item with id - {str(id)!r} deleted"}
        return {"success": False, "message": f'Item with id - {str(id)!r} does not exist!'}

    async def get_by_name(self, name: str):
        if db_model := await self._context.get_by_name(name):
            return db_model
        else:
            return {"status": False, "message": f"Item with name - {name!r} does not exist!"}

    async def update_by_name(self, name: str, put_data):
        try:
            db_model = await self._context.update_by_name(name, **put_data.model_dump())
        except IntegrityError:
            return {"success": False, "message": "Item with this name already exists, names need be unique!"}
        if db_model is None:
            return {"status": False, "message": f"Item with name - {name!r} does not exist!"}
        await self._context.save_changes()
        return db_model

    async def delete_by_name(self, name: str):
        if await self._context.delete_by_name(name):
            await self._context.save_changes()
            return {'success': True, "message": f"Item with name - {name!r} deleted"}
        return {"success": False, "message": f'Item with id - {name!r} does not exist!'}

    async def create_many(self, post_data):
        try:
            weapon_db_models = await self._context.create_many([post_model.model_dump() for post_model in post_data])
        except IntegrityError:
            return {"success": False, "message": "Item names should be unique!"}
        await self._context.save_changes()
        return weapon_db_models

    async def delete_many_by_id(self, ids: typing.List[int]):
        existence_db_models = await self._context.get_many_by_id(ids)
        ids_on_delete = [model.id for model in existence_db_models]
        not_found_ids = [id for id in ids if id not in ids_on_delete]
        if ids_on_delete:
            await self._context.delete_many_by_id(ids_on_delete)
            await self._context.save_changes()
            return {
                'success': True,
                'message': f'Items with {ids_on_delete} deleted. {f'{not_found_ids} not found' if not_found_ids else ''}'}
        return {"success": False, "message": f"Items with {ids} not found"}

    async def delete_many_by_name(self, names: typing.List[str]):
        print(names)
        existence_db_models = await self._context.get_many_by_name(names)
        names_on_delete = [model.name for model in existence_db_models]
        print(names_on_delete)
        not_found_names = [name for name in names if name not in names_on_delete]
        if names_on_delete:
            await self._context.delete_many_by_name(names_on_delete)
            await self._context.save_changes()
            return {
                'success': True,
                'message': f'Items with name {names_on_delete} deleted. {f'{not_found_names} not found' if not_found_names else ''}'
            }
        return {"success": False, "message": f"Items with names {names} not found"}


def weapon_end_point_executor(context: Table = fastapi.Depends(database.get_db_weapon_context)):
    return CommonEndPointExecutor(context)


def skin_end_point_executor(context: Table = fastapi.Depends(database.get_db_skin_context)):
    return CommonEndPointExecutor(context)


def quality_end_point_executor(context: Table = fastapi.Depends(database.get_db_quality_context)):
    return CommonEndPointExecutor(context)