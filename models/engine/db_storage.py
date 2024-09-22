#!/usr/bin/python3
"""
class DBStorage to interect with database
"""

import models
import sqlalchemy
from models.base_model import BaseModel, Base
from models.user import User
from models.review import Review
from models.service import Service
from models.artisan import Artisan
from models.booking import Booking
from models.subservice import SubService
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"User": User, "Service":Service, "Artisan":Artisan, "Review":Review, "Booking":Booking, "SubService":SubService}

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine("sqlite:///craftdot.db")

    def reload(self):
        """reload data from database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session
    
    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """save objects to database"""
        self.__session.commit()

    def close(self):
        """Close database session"""
        self.__session.remove()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

    def get_user_with_phone_no(self, phone_number):
        """
        Returns the user based on the phone number
        """
        all_users = models.storage.all(User)
        for user in all_users.values():
            if (user.phone_number == phone_number):
                return user
           
            
    def get_user_with_email(self, email):
        """
        Returns the user based on the email
        """
        all_users = models.storage.all(User)
        for user in all_users.values():
            if (user.email == email):
                return user

    def get_s(self, name):
        """
        Returns the service based on the name
        """
        all_services = models.storage.all(Service)
        for service in all_services.values():
            if (service.name == name):
                return service

            
    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count
        

