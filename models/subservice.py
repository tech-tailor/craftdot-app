#!/usr/bin/python3
""" Sub service model"""


import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class SubService(BaseModel, Base):
    """create different service categories"""
    __tablename__ = "subservices"
    service_id = Column(String(60), ForeignKey('services.id'), nullable=False) 
    name = Column(String(128), unique=True, nullable=False)
    description = Column(String(256), nullable=True)
    picture = Column(String(128), nullable=True)
    service = relationship('Service', back_populates='subservices')

    def __init__(self, *args, **kwargs):
        """initialise the user model"""
        super().__init__(*args, **kwargs)