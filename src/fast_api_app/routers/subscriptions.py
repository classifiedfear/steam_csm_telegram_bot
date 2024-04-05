import fastapi

from src.fast_api_app.dependencies.db import get_db_all_tables

subscription_router = fastapi.APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"],
    dependencies=[fastapi.Depends(get_db_all_tables)]
)