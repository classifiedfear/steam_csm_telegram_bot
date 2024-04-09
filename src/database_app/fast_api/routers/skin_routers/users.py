import fastapi

from src.database_app.fast_api.dependencies.database import get_db_context

user_router = fastapi.APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[fastapi.Depends(get_db_context)]
)