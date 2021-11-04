import typer
import asyncio
import uvicorn
# from fastapi_migrations import MigrationsConfig, Migrations
# from fastapi_migrations.cli import MigrationsCli

# from fastapi_sqlalchemy import DBSessionMiddleware
from app.main import create_dev_app
from app.config import settings
from app.models.dbconnect import async_main
capp = typer.Typer()
app=create_dev_app()
# app.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_MIGRATION_URI)


#this is for creating models 
@capp.command()
def upgrade():
    asyncio.run(async_main())

# this is for testing app
@capp.command()
def test():
    typer.run('pytest -v')
@capp.command()
def run():
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")

if __name__ == "__main__":
    capp()

# 