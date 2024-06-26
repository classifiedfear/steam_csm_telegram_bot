from src.database_app.database.context.bot_database_context import BotDatabaseContext, BotDatabaseEngine

url = (
            f'postgresql+asyncpg://'
            f'classified:rv9up0ax@classified-pi:'
            f'5432/tg_skins_bot_db'
        )
engine = BotDatabaseEngine(url)


async def get_db_context():
    async with BotDatabaseContext(engine) as context:
        yield context


async def get_db_weapon_context():
    async with BotDatabaseContext(engine) as context:
        yield context.get_weapon_table()


async def get_db_skin_context():
    async with BotDatabaseContext(engine) as context:
        yield context.get_skin_table()


async def get_db_quality_context():
    async with BotDatabaseContext(engine) as context:
        yield context.get_quality_table()


async def get_db_wsq_context():
    async with BotDatabaseContext(engine) as context:
        yield context.get_weapon_skin_quality_table()


async def get_db_user_context():
    async with BotDatabaseContext(engine) as context:
        yield context.get_user_table()


async def get_db_subscription_context():
    async with BotDatabaseContext(engine) as database:
        yield