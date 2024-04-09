import fastapi

from src.database_app.fast_api.dependencies.database import get_db_context

subscription_router = fastapi.APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"],
    dependencies=[fastapi.Depends(get_db_context)]
)