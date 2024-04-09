import sqlalchemy

from src.database_app.database.tables.abc_table.table import Table


class SubscriptionTable(Table):
    def method(self):
        select_stmt = sqlalchemy.select(users_models.Subscription).group_by(
            users_models.Subscription.weapon_id,
        )
