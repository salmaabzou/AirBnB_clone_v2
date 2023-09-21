#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
import shlex


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Return a dic"""
        myDiction = {}
        seconddic = self.__objects
        if cls:
            clsName = cls.__name__
            for k in seconddic:
                prtion = k.replace('.', ' ')
                prtion = shlex.split(prtion)
                if (prtion[0] == clsName):
                    secddic = self.__objects
                    myDiction[k] = secddic[k]
            return (myDiction)
        else:
            return seconddic

    def delete(self, obj=None):
        ''' deletes the object from the attribute
        '''
        if obj is None:
            return
        objDic = obj.to_dict()['__class__']
        kyOb = objDic + '.' + obj.id
        allKeys = self.__objects.keys()
        if kyOb in allKeys:
            objTODel = self.__objects[kyOb]
            del objTODel

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass