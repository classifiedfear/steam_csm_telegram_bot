import fastapi

from src.database_app.services.bot_database_refresher.bot_database_refresher import BotDatabaseRefresher
from src.database_app.fast_api.dependencies import database
from src.database_app.database.context.bot_database_context import BotDatabaseContext


update_db_router = fastapi.APIRouter(
    prefix="/update_db",
    tags=["update_db"],
    dependencies=[fastapi.Depends(database.get_db_context)]
)


@update_db_router.post("")
async def update_db(request: fastapi.Request, context: BotDatabaseContext = fastapi.Depends(database.get_db_context)):
    db_service = BotDatabaseRefresher(context)
    await db_service.refresh(await request.body())



