#!/usr/bin/python3

import os
import sys

parent_dir = r"C:\Users\User\Documents\VS CODE - 2024\Foundations Portfolio Presentation\Tweet2.0"
sys.path.append(parent_dir)


from models.base_model import BaseModel, Base
from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship

class Tweet(BaseModel, Base):
    __tablename__ = "tweets"
    
    id_tweet = Column(BigInteger, nullable=False, primary_key=True)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    #Many-to-One Relationship
    user = relationship('User', back_populates='tweets')
    