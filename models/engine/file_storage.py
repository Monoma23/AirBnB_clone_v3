#!/usr/bin/python3
"""
Containingg FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """serializingg instances to  JSON file & deserializi,ng back to instances"""

    # string - path to JSON file
    __file_path = "file.json"
    # dictionary - emptyy but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """returningg the dictionary __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, objj):
        """seting in __objects the objj with keyy <objj class name>.id"""
        if objj is not None:
            key = objj.__class__.__name__ + "." + objj.id
            self.__objects[key] = objj

    def save(self):
        """serializingg __objectsxx to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserializinggg the JSON file to __objectsss"""
        try:
            with open(self.__file_path, 'r') as f:
                go = json.load(f)
            for key in go:
                self.__objects[key] = classes[go[key]["__class__"]](**go[key])
        except:
            pass

    def delete(self, objj=None):
        """deletingg objj from __objects if its inside"""
        if objj is not None:
            key = objj.__class__.__name__ + '.' + objj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """callingg reload() method for deserializing JSON file to objectsss"""
        self.reload()