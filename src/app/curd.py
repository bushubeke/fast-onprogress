import asyncio
from fastapi import APIRouter,FastAPI,Request,Form,Body,Depends
from sqlalchemy.orm import declarative_base as Base, sessionmaker
from pydantic import BaseModel,EmailStr,Field
from typing import List,Dict,Tuple,Optional
from passlib.hash import pbkdf2_sha512
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

#lst3 = [value for value in lst1 if value in lst2]
class sqlalchemycurd:
    #
    def __init__(self, app : FastAPI = None, session : AsyncSession=None ):
        self.combmodels : List[List[Base,BaseModel]] = []
        self.app : FastAPI = None
        self.session : sessionmaker = None
        self.curdroute=APIRouter()
        self.engine: create_async_engine=None
        if app is not None and engine is not None:
            init_app(app,session,engine)
    # inistializing init app 
    def init_app(self, app : FastAPI = None,engine : create_async_engine= None):
        if app is not None and engine is not None:
            self.app = app
            self.engine=engine
            self.session = sessionmaker(engine, expire_on_commit=False,class_=AsyncSession)
            
    # Dependency
    async def get_session(self,) -> AsyncSession:

          async with self.session() as session:
               yield session
    
    
    
    def add_curd(self, modlist):
    #    specroute=self.curdroute
         if modlist  is not None :
              self.combmodels=modlist 
              #print(self.combmodels) 
         self.create_routes()
    

    async def get_all(request: Request):
         return { f"Message" : f"This is get_all GET request route "}
    
    async def get_one(request: Request,whatever:Optional[str]):
         return { f"Message" : f"This is get_all GET request route {whatever} "}
    
    def post_one(self,request: Request,sqlmod : Base, pyMod : BaseModel):
              current_sql_model=sqlmod
              curmod=pyMod
              
              
              get_session=self.get_session
              async def post_response(request : Request, mod : curmod, session : AsyncSession=Depends(get_session)):
                   #print(current_sql_model.tableroute())
                   #print("2 \n")
                   data=dict(mod)
                   
                   if data.get("password") is not None:
                        
                        data["password"]=pbkdf2_sha512.using(rounds=25000,salt_size=80).hash(data['password'])
                   try:
                        #print("3 \n")
                        db_model_value=current_sql_model(**data)
                        #print("4 \n")
                        session.add(db_model_value)
                        await session.commit()
                        #session.refresh(db_model_value)
                        #print("5 \n")
                        
                   except Exception as e :
                         #print("6 \n")
                         print(e)
                         await session.rollback()
                         #print("7 \n")
                        
                   finally: 
                         #print("8 \n")
                         await session.close()
                         #print("9 \n")
                   #print("10 \n")
                   return data
              return post_response
         #return givenMod
    
    async def put_one(request: Request):
         return { f"Message" : f"This is get_all GET request route "}
    
    async def delete_one(request: Request):
         return { f"Message" : f"This is get_all GET request route "}
    
    async def delete_all(request: Request):
         return { f"Message" : f"This is get_all GET request route "}



    def create_routes(self,)-> None:
        xroute=self.curdroute
        #xroute.add_api_route(f"/{self.combmodels[0][0].tableroute()}/{{whatever}}",self.get_one, methods=["GET"])
        for x in self.combmodels:
            xroute.add_api_route(f"/{x[0].tableroute()}/all", self.get_all , methods=["GET"])
            xroute.add_api_route(f"/{x[0].tableroute()}/{{whatever}}", self.get_one,methods=["GET"])
            xroute.add_api_route(f"/{x[0].tableroute()}",self.post_one(self,x[0],x[1]), methods=["POST"])
            xroute.add_api_route(f"/{x[0].tableroute()}/{{whatever}}",self.put_one, methods=["PUT"])
            xroute.add_api_route(f"/{x[0].tableroute()}/{{whatever}}",self.delete_one, methods=["DELETE"])
            xroute.add_api_route(f"/{x[0].tableroute()}/all",self.delete_all, methods=["DELETE"])
        self.app.include_router(xroute)