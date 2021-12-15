#pip install SQLAlchemy==1.4.3 aiosqlite
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
import asyncio
# from ..config import settings
# DATABASE_URL = "postgresql+asyncpg://postgres:yahweh@stip/development-template"

engine = create_engine('postgresql+psycopg2://postgres:yahweh@192.168.10.3:5432/development-template',convert_unicode=True, future=True, echo=True)
asyncengine=create_async_engine('postgresql+asyncpg://postgres:yahweh@192.168.10.3:5432/development-template',convert_unicode=True)
#db_session=sessionmaker(autocommit=False,autoflush=False,bind=syncengine)
# async_session = sessionmaker(asyncengine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()   

async def async_main():
    #engine = create_async_engine(DATABASE_URL, future=True, echo=True)

    async with asyncengine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


######################################################
async def droptables():
    async with asyncengine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
######################################################