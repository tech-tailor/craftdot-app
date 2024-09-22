#!/usr/bin/python3
"""category model"""


import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

class Review(BaseModel, Base):
    """create different service categories"""
    __tablename__ = "reviews"
    service_id = Column(String(60), ForeignKey('services.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    booking_id = Column(Integer, ForeignKey('bookings.id'), nullable=True)
    artisan_id = Column(Integer, ForeignKey('artisans.id'), nullable=True)
    comment = Column(String(1024), nullable=True)
    rating = Column(Integer, nullable=False)
    user = relationship("User", uselist=False, back_populates="reviews")
    artisan = relationship("Artisan", uselist=False, back_populates="reviews")
    booking = relationship("Booking", uselist=False, back_populates="review")
    service = relationship("Service", uselist=False, back_populates="reviews")

    def __init__(self, *args, **kwargs):
        """initialise the user model"""

        super().__init__(*args, **kwargs)