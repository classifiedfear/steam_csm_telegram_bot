from src.database_app.fast_api.routers.skin_routers.weapons import weapon_router
from src.database_app.fast_api.routers.skin_routers.skins import skin_router
from src.database_app.fast_api.routers.skin_routers.quality import quality_router
from src.database_app.fast_api.routers.skin_routers.wsq import wsq_router
from src.database_app.fast_api.routers.skin_routers.users import user_router
from src.database_app.fast_api.routers.user_routers.subscriptions import subscription_router
from src.database_app.fast_api.routers.service_routers.update_db import update_db_router

__all__ = [
    'weapon_router', 'skin_router', 'quality_router', 'wsq_router',
    'user_router', 'subscription_router', 'update_db_router'
]

routers = [
    weapon_router, skin_router, quality_router, wsq_router,
    user_router, subscription_router, update_db_router
]