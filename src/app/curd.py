import asyncio
from fastapi import APIRouter,FastAPI,Request,Form,Body,Depends
from sqlalchemy import select,update,delete
from sqlalchemy.orm import declarative_base as Base, session, sessionmaker
from pydantic import BaseModel,EmailStr,Field
from typing import ClassVar, List,Dict,Tuple,Optional
from passlib.hash import pbkdf2_sha512
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import uuid

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
    

    def get_all(self,request:Request,sqlmod : Base):
         current_sql_model=sqlmod
         
         get_session=self.get_session
         async def get_all_response(request:Request,session : AsyncSession=Depends(get_session)):
              try:
                print('###1')
                cur_model= await session.execute(select(current_sql_model))
                cur_model=cur_model.scalars().all()
                print(cur_model)
                print('###2')
                return cur_model
              except Exception as e:
                print(e)
                await session.rollback()
                return {"Message": "some Error Occured"}
              finally:
                print('The try except is finished')
         return get_all_response
    
    def get_one(self,request:Request,sqlmod : Base,item_uuid:Optional[uuid.uuid4]=None):
         current_sql_model=sqlmod
         
         get_session=self.get_session
         async def get_one_response(request:Request,item_uuid,session : AsyncSession=Depends(get_session)):
              
               try:
                 curr_model=await session.execute(select(current_sql_model).filter_by(id=item_uuid))
                 curr_model=curr_model.scalars().first()
               
                 return curr_model
               except Exception as e:
                 print(e)
                 return {"Message":"Some Error Occured"}
                 
               finally:
                 await session.close()
                   
               
                
         return get_one_response    
    def post_one(self,request: Request,sqlmod : Base, pyMod : BaseModel):
              current_sql_model=sqlmod
              curmod=pyMod
              
              
              get_session=self.get_session
              async def post_response(request : Request,mod : curmod,session : AsyncSession=Depends(get_session)):
                   
                   data=dict(mod)
                   print(data)                  
                   try:
                        
                        db_model_value=current_sql_model(**data)
                        print(db_model_value.password)
                        print("4 \n")
                        session.add(db_model_value)
                        await session.commit()
                                            
                        
                   except Exception as e :
                         
                         print(e)
                         await session.rollback()
                         
                        
                   finally: 
                         
                         await session.close()
                         
                   
                   return {"Message":"insert has been sucessful"}
              return post_response

    def put_one(self,request:Request,sqlmod : Base, pyMod : BaseModel,item_uuid:Optional[uuid.uuid4]=None):
          
          current_sql_model=sqlmod
          curmod=pyMod
                     
          get_session=self.get_session
          async def put_response(request : Request,item_uuid,mod : curmod, session : AsyncSession=Depends(get_session)):
             
               data=dict(mod)
              
               try:
                    
                    await session.execute(update(current_sql_model).where(current_sql_model.id==item_uuid).values(**data))
                    print("####3")
                    await session.commit()
                    return { f"Message" : f"sucessfully updated object "}
               except Exception as e:
                    print(e)
                    await session.rollback()
                    return { f"Message" : f"failed to sucessfully update object "}
               finally:
                    await session.close()
              
          return put_response          
    def delete_one(self,request:Request,sqlmod : Base,item_uuid:Optional[uuid.uuid4]=None):
          current_sql_model=sqlmod

          get_session=self.get_session
          async def delete_one_response(request : Request,item_uuid, session : AsyncSession=Depends(get_session)):
               
               try:
               
                 await session.execute(delete(current_sql_model).where(current_sql_model.id == item_uuid))
                 await session.commit()
                 return {"Message" :"Sucessfully Deleted object"}
               except Exception as e:
                    await session.rollback()
                    return {"Message":"Failled to Sucessfully Delete object "}
 
               finally:
                 await session.close()
               
          return delete_one_response
        
    async def delete_all(request: Request):
         return { f"Message" : f"This is get_all GET request route "}



    def create_routes(self,)-> None:
        xroute=self.curdroute
        #xroute.add_api_route(f"/{self.combmodels[0][0].tableroute()}/{{whatever}}",self.get_one,response_model=x[1], methods=["GET"])
        for x in self.combmodels:
            xroute.add_api_route(f"/{x[0].tableroute()}/all", self.get_all(self,x[0]),methods=["GET"])
            xroute.add_api_route(f"/{x[0].tableroute()}/{{item_uuid}}", self.get_one(self,x[0]),response_model=x[1],methods=["GET"])
            xroute.add_api_route(f"/{x[0].tableroute()}",self.post_one(self,x[0],x[1]), methods=["POST"])
            xroute.add_api_route(f"/{x[0].tableroute()}/{{item_uuid}}",self.put_one(self,x[0],x[1]), methods=["PUT"])
            xroute.add_api_route(f"/{x[0].tableroute()}/{{item_uuid}}",self.delete_one(self,x[0]), methods=["DELETE"])
            xroute.add_api_route(f"/{x[0].tableroute()}/all",self.delete_all, methods=["Delete"])
        self.app.include_router(xroute)