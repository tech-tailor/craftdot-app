#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.users import *
from api.v1.views.artisans import *
from api.v1.views.bookings import *
from api.v1.views.services import *
from api.v1.views.reviews import *
from api.v1.views.index import *
from api.v1.views.subservices import *
from api.v1.views.verification import *