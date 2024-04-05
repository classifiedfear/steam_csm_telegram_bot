from .weapons import weapon_router
from .skins import skin_router
from .quality import quality_router
from .wsq import wsq_router
from .users import user_router
from .subscriptions import subscription_router
from .update_db import update_db_router

__all__ = [
    'weapon_router', 'skin_router', 'quality_router', 'wsq_router',
    'user_router', 'subscription_router', 'update_db_router'
]

routers = [
    weapon_router, skin_router, quality_router, wsq_router,
    user_router, subscription_router, update_db_router
]