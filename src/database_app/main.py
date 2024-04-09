
import fastapi
from src.database_app.fast_api import routers

app = fastapi.FastAPI()
for router in routers.routers:
    app.include_router(router)
