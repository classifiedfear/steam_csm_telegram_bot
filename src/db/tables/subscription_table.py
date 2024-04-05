import sqlalchemy
from sqlalchemy.dialects import postgresql

from src.db.models import users_models
from src.db.tables.table import Table


class SubscriptionTable(Table):
    def method(self):
        select_stmt = sqlalchemy.select(users_models.Subscription).group_by(
            users_models.Subscription.weapon_id,
        )
