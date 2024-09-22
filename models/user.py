#!/usr/bin/python3
"""user model"""

import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Enum
import enum
from sqlalchemy.orm import relationship
from hashlib import md5
from bcrypt import hashpw, gensalt, checkpw

class RoleEnum(enum.Enum):
    admin1 = 'admin1'
    admin2 = 'admin2'
    artisan = 'artisan'
    user = 'user'


class User(BaseModel, Base):
    """User model that entails every details"""

    
    __tablename__ = "users"
    phone_number = Column(String(128), unique=True, nullable=True)
    email = Column(String(128), unique=True, nullable=True)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    longitude = Column(String(128), nullable=True)
    latitude = Column(String(128), nullable=True)
    street_address = Column(String(255), nullable=True)
    lga = Column(String(128), nullable=True)
    state = Column(String(128), nullable=True)
    country = Column(String(128), nullable=True, default="Nigeria")
    profile_picture = Column(String(128), nullable=True)
    role = Column(String(20), default=RoleEnum.user.value) # 1 admin1, 2 for admin2, 3 for artisan, 4 user 
    artisan = relationship("Artisan", uselist=False, back_populates="user")
    reviews = relationship("Review", uselist=True, back_populates="user")
    bookings = relationship("Booking", uselist=True, back_populates="user")
    #services = relationship("Service", uselist=True, back_populates="users")


    def __init__(self, *args, **kwargs):
        """initialise the user model"""
        super().__init__(*args, **kwargs)

    def just_show(self):
        return self.password

    def __setattr__(self, name, value):
        """sets a password with bycrypt encryption"""
        if name == "password":
            value = self.hash_password(value) #md5(value.encode()).hexdigest()
        super().__setattr__(name, value)

    def hash_password(self, password):
        return hashpw(password.encode(), gensalt()).decode()
    
    def check_password(self, password):
        """Check if the password is correct"""
        return checkpw(password.encode(), self.password.encode())
    
    def set_password(self, new_password):
        self.password = self.hash_password(new_password)
