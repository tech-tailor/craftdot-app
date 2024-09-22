#!/usr/bin/python3
"""artisian model"""


import models
from models.user import User
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Artisan(BaseModel, Base):
    """User model that entails every details"""
    __tablename__ = "artisans"
    user_id = Column(String(60), ForeignKey('users.id'), unique=True, nullable=False)
    service_id = Column(String(60), ForeignKey('services.id'),  unique=True, nullable=True)
    #booking_id = Column(String(60), ForeignKey('bookings.id'),  unique=True, nullable=False)
    #review_id = Column(String(60), ForeignKey('reviews.id'),  unique=True, nullable=False)
    skills = Column(String(128), nullable=True)
    experience = Column(String(128), nullable=True)
    availability = Column(String(128), nullable=True)
    pricing = Column(String(128), nullable=True)
    user = relationship("User", uselist=False, back_populates="artisan")
    service = relationship("Service", uselist=False, back_populates="artisans")
    bookings = relationship("Booking", uselist=True, back_populates="artisan")
    reviews = relationship("Review", uselist=True, back_populates="artisan")

    def __init__(self, *args, **kwargs):
        """initialise the user model"""
        super().__init__(*args, **kwargs)
        