#!/usr/bin/python3
"""File storage """

import json
import os
from models.base_model import BaseModel

classes = {"BaseModel": BaseModel}

class FileStorage:
    __file_path = "file.json"

    __objects = {}

    def __init__(self):
        pass

    # Save into the file
    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            if key == "password":
                json_objects[key].decode()
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)
            return "file saved successfully"

    def all(self):
        reload()
        return self.__objects
        
    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                loaded_file = json.load(f)
            for key in jo:
                self.__objects[key] = classes[loaded_file[key]["__class__"]](**loaded_file[key])
        except:
            pass
    
    def new(self, obj):
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]


    

    

    
