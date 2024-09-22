#!/usr/bin/python3
"""category model"""


import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship

class Service(BaseModel, Base):
    """create different service categories"""
    __tablename__ = "services"
    name = Column(String(128), unique=True, nullable=False)
    description = Column(String(256), nullable=True)
    service_picture = Column(String(128), nullable=True)
    service_icon = Column(String(128), nullable=True)
    subservices = relationship('SubService', back_populates='service')
    #user_id = Column(String(60), ForeignKey('users.id'))
    artisans = relationship("Artisan", uselist=True, back_populates="service")
    reviews = relationship("Review", uselist=True, back_populates="service")
    bookings = relationship("Booking", uselist=True, back_populates="service")
    #users = relationship("User", uselist=True, back_populates="services")

    def __init__(self, *args, **kwargs):
        """initialise the user model"""
        super().__init__(*args, **kwargs)