#!/usr/bin/python3

import os
import sys

parent_dir = r"C:\Users\User\Documents\VS CODE - 2024\Foundations Portfolio Presentation\Tweet2.0"
sys.path.append(parent_dir)

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel, Base):
    __tablename__ = "users"
    
    email = Column(String(128), nullable=False, unique=True, index=True)
    username = Column(String(128), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
    
    # One-to-Many Relationship 
    tweets = relationship('Tweet', back_populates='user', cascade="all, delete-orphan")
    
    

