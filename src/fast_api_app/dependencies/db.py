from src.db.bot_database import BotDatabase, BotDatabaseEngine

def get_db_engine() -> BotDatabaseEngine:
    url = (
            f'postgresql+asyncpg://'
            f'classified:rv9up0ax@classified-pi:'
            f'5432/tg_skins_bot_db'
        )
    return BotDatabaseEngine(url)


async def get_db_all_tables():
    engine = get_db_engine()
    await engine.drop_all_tables()
    await engine.proceed_schemas()
    async with BotDatabase(engine) as database:
        yield database

async def get_db_weapon_table():
    engine = get_db_engine()
    async with BotDatabase(engine) as database:
        yield database.get_weapon_table()

async def get_db_skin_table():
    engine = get_db_engine()
    async with BotDatabase(engine) as database:
        yield database.get_skin_table()

async def get_db_quality_table():
    engine = get_db_engine()
    async with BotDatabase(engine) as database:
        yield database.get_quality_table()

async def get_db_wsq_table():
    engine = get_db_engine()
    async with BotDatabase(engine) as database:
        yield database.get_weapon_skin_quality_table()

async def get_db_user_table():
    engine = get_db_engine()
    async with BotDatabase(engine) as database:
        yield database.get_user_table()

async def get_db_subscription_table():
    engine = get_db_engine()
    async with BotDatabase(engine) as database:
        yield