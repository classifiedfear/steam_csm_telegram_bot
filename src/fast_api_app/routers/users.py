import fastapi

from src.fast_api_app.dependencies.db import get_db_all_tables

user_router = fastapi.APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[fastapi.Depends(get_db_all_tables)]
)