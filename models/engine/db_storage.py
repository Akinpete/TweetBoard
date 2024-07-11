#!/usr/bin/python3

import os

import sys

parent_dir = r"C:\Users\User\Documents\VS CODE - 2024\Foundations Portfolio Presentation\Tweet2.0"
sys.path.append(parent_dir)

# from dotenv import load_dotenv
# load_dotenv()

database_url = os.getenv('DATABASE_URL')

from models.base_model import BaseModel, Base
from models.user import User
from models.tweet import Tweet
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

class DBStorage:
    __engine = None
    __session = None
    
    def __init__(self):
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        envi = os.getenv('HBNB_ENV')
        
        self.__engine= create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(user, pwd, host, db), pool_pre_ping=True)
        
    
    def all(self, cls=None):
        from models.user import User
        from models.tweet import Tweet
        
        classes = {
            "Tweet": Tweet,
            "User": User    
        }
        
        obj_dict = {}
        if cls:
            if isinstance(cls, str):
                cls = classes.get(cls)
            if cls:
                try:
                    objs = self.__session.query(cls).all()
                except sqlalchemy.exc.InvalidRequestError:
                    # This handles cases where a relationship might not exist
                    return
                for obj in objs:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    obj_dict[key] = obj
        else:
            for class_name, class_ref in classes.items():
                objs = self.__session.query(class_ref).all()
                for obj in objs:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    obj_dict[key] = obj
    
        return obj_dict
    
    def new(self, obj):
        """add the object to the current database session"""
        print("Adding object to session:", obj.__dict__)
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)
            
    def reload(self):        
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
        
    def close(self):
        self.__session.close()
        
    def drop_all_tables(self):
        """Drop all tables in the database."""        
        Base.metadata.drop_all(self.__engine)
        print("All tables dropped.")
    
        
        




