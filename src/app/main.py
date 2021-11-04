
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .curd import sqlalchemycurd
from .models.dbconnect import asyncengine
# from .models.dbconnect import async_session,engine
from .models.dbmodels import Role,RoleModel,User,UserModel

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sqlcurd=sqlalchemycurd()
def create_dev_app():
    app=FastAPI()
    sqlcurd.init_app(app,asyncengine)
    
    modlist=[[User,UserModel],[Role,RoleModel]]
    #modlist=[[Role,RoleModel]]
    sqlcurd.add_curd(modlist)
    #sqlcurd.add_curd(Role,RoleModel)
    templates = Jinja2Templates(directory="templates")
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    @app.get("/")
    def index():
        return {"Message":"You should make your own index page"}

    return app


def create_prod_app():
    app=FastAPI()
    
    app.mount("/static", StaticFiles(directory="/app/static"), name="static")    