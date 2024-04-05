
import fastapi
from . import routers

app = fastapi.FastAPI()
for router in routers.routers:
    app.include_router(router)