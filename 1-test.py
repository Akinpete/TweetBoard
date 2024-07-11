#!/usr/bin/python3

from models.base_model import BaseModel
obj1 = BaseModel()
obj1.name = 'emmanuel'
print(obj1.to_dict())