import fastapi

from src.fast_api_app.dependencies.db import get_db_all_tables

wsq_router = fastapi.APIRouter(
    prefix="/wsq",
    tags=["wsq"],
    dependencies=[fastapi.Depends(get_db_all_tables)]
)