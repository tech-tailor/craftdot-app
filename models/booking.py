#!/usr/bin/python3
"""booking model"""


import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship

class Booking(BaseModel, Base):
    """Booking model, book a service"""
    __tablename__ = "bookings"
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    artisan_id = Column(String(60), ForeignKey('artisans.id'), nullable=False)
    service_id = Column(String(60), ForeignKey('services.id'), nullable=False)
    payment_info = Column(String(128), nullable=True)
    status = Column(String(128), nullable=False, default='Pending')
    user = relationship("User", uselist=False, back_populates="bookings")
    artisan = relationship("Artisan", uselist=False, back_populates="bookings")
    service = relationship("Service", uselist=False, back_populates="bookings")
    review = relationship("Review", uselist=False, back_populates="booking")

    def __init__(self, *args, **kwargs):
        """initialise the user model"""
        super().__init__(*args, **kwargs)