import fastapi

from src.database_app.fast_api.dependencies.database import get_db_context

wsq_router = fastapi.APIRouter(
    prefix="/wsq",
    tags=["wsq"],
    dependencies=[fastapi.Depends(get_db_context)]
)