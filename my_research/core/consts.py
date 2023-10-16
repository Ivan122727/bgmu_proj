import asyncio

from my_research.db.db import DB
from my_research.core.settings import Settings

settings = Settings()
db = DB(mongo_uri=settings.mongo_uri, mongo_db_name=settings.mongo_db_name)
