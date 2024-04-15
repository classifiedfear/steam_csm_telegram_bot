import fastapi
from src.database_app.fast_api.routers import *

routers = [
    weapon_router, skin_router, quality_router, user_router, subscription_router, relation_router, update_db_router
]


app = fastapi.FastAPI()
for router in routers:
    app.include_router(router)
