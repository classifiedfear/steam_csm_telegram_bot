import asyncio

from src.services.cs_skins_data_retriever.cs_skin_data_retriever import CsInfoService
from src.scheduler_tasks.db_data_updater.database_updater import DbUpdater

from src.services.misc.common_request_executor import CommonRequestExecutor


async def main():
    request_executor = CommonRequestExecutor()
    #url = (
    #    f'postgresql+asyncpg://'
    #    f'{os.getenv('postgres_user')}:{os.getenv('postgres_password')}@{os.getenv('host')}:'
    #    f'{os.getenv('postgres_port')}/{os.getenv('postgres_db_name')}'
    #)
    service = CsInfoService()
    #database = BotDatabaseEngine(url)
    #await database.drop_all_tables()
    #await database.proceed_schemas()
    filler = DbUpdater(service)
    await filler.update()

asyncio.run(main())
