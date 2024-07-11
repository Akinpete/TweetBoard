#!/usr/bin/python3

import os
import sys

parent_dir = r"C:\Users\User\Documents\VS CODE - 2024\Foundations Portfolio Presentation\Tweet2.0"
sys.path.append(parent_dir)

import models
from models.base_model import BaseModel, Base
from models.tweet import Tweet
from models.user import User
from models import storage

# creation of a User
user1 = User(email="aki@gmail", username="California", hashed_password="123dfg")
user1.save()

# creation of a User
user2 = User(email="uku@gmail", username="Americurrr", hashed_password="321ghj")
user2.save()

# creation of a User
user3 = User(email="omi@gmail", username="Laliga", hashed_password="hmm500")
user3.save()

# creation of different tweets
tweet1 = Tweet(id_tweet=123456789, user_id = user1.id)
tweet2 = Tweet(id_tweet=543324555, user_id = user2.id)
tweet3 = Tweet(id_tweet=678048339, user_id = user3.id)
tweet4 = Tweet(id_tweet=233456466, user_id = user1.id)
tweet5 = Tweet(id_tweet=345566543, user_id = user2.id)
tweet5 = Tweet(id_tweet=123098333, user_id = user3.id)
tweet6 = Tweet(id_tweet=897603517, user_id = user1.id)

storage.new(tweet1)
storage.new(tweet2)
storage.new(tweet3)
storage.new(tweet4)
storage.new(tweet5)

storage.save()

print("OK")