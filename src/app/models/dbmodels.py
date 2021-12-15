from .dbconnect import Base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer,String, ForeignKey
# import datetime
# from datetime import tzinfo, timedelta, datetime
from sqlalchemy.sql import func
import uuid
from typing import List, Optional
from pydantic import BaseModel,EmailStr
# from fastapi import Form  
from sqlalchemy.dialects.postgresql import ENUM, JSON,UUID
from sqlalchemy.ext.mutable import MutableDict
###########################################################################
# ZERO = timedelta(0)

# class UTC(tzinfo):
#   def utcoffset(self, dt):
#     return ZERO
#   def tzname(self, dt):
#     return "UTC"
#   def dst(self, dt):
#     return ZERO

# utc = UTC()

#############################################################################
    #this is roles table along with its methods
############################################################################
class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True,autoincrement="auto")
    name = Column(String(80), unique=True)
    description = Column(String(255))

    def __repr__(self):
        return f"{self.name}"
    @staticmethod
    def tableroute():
        return "role"

class RoleModel(BaseModel):
    
    name : str 
    description : Optional[str]
    
    class Config:
        orm_mode = True
#############################################################################


###########################################################################
    #this is the user method along with the user model methods
##########################################################################
class User(Base):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email=Column(String(255), unique=True,nullable=False)
    username =Column(String(100),unique=True,nullable=False)
    first_name =Column(String(100),nullable=False)
    middle_name = Column(String(100),nullable=False)
    last_name= Column(String(100),nullable=False)
    password = Column(String(500),nullable=False)
    # date_registerd=Column(DateTime(),default=datetime.datetime.now().astimezone())
    date_registerd=Column(DateTime(timezone=True), default=func.now())
    confirmed_at=Column(DateTime(),nullable=True)
    active = Column(Boolean(),default=False)
    roles = relationship('Role', secondary='roles_users',backref=backref('users',cascade="all", lazy='dynamic'))
            
    #pbkdf2_sha512.verify(password,self.password_hash)


    def __repr__(self):
        return f"<User '{self.username}'>"

    @staticmethod
    def tableroute():
        return "user"

class UserModel(BaseModel):
    email : EmailStr 
    username: str
    first_name : str
    middle_name : Optional[str] = None 
    last_name : str 
    password : str 
    # date_registerd : datetime.datetime
    # confirmed_at : Optional[datetime.datetime] 
    active :Optional[bool] 
    
    class Config:
        orm_mode = True
###########################################################################
    #this is for many to many roles models relationship 
############################################################################
class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id',UUID(as_uuid=True) , ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))
    #users = relationship('User',backref=backref('users', lazy='dynamic'))

    def __repr__(self):
        return f"<UserRole '{self.role_id}'>"
###########################################################################
    #this is for many to many roles models relationship 
############################################################################