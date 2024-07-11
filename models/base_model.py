#!/usr/bin/python3

from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy.ext.declarative  import declarative_base
from sqlalchemy import Column, String, DateTime
import uuid

Base = declarative_base()

class BaseModel:
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at =  Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    def __init__(self, *args, **kwargs):
        """Instantiates the new base model"""
        if kwargs:
            if '__class__' in kwargs:
                del kwargs['__class__']
            for key, value in kwargs.items():
                if key in ('created_at', 'updated_at'):
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                    # kwargs[key] = datetime.fromisoformat(value)
                    
                setattr(self, key, value)
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                self.created_at = datetime.now()
            if 'updated_at' not in kwargs:
                self.updated_at = self.created_at
        else:
            print("Creating new instance with default values")            
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            print(f"finished Object: {self.__dict__}")
            
    def __str__(self):
        """String representation of an instance"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)
    
            

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        from models import storage
        storage.new(self)
        storage.save()
        
    def delete(self):
        """delete the current instance from the storage"""
        from models import storage
        storage.delete(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format with class name added"""
        new_dict = self.__dict__.copy()
        new_dict['__class__'] = self.__class__.__name__
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in new_dict:
            del new_dict['_sa_instance_state']

        return new_dict