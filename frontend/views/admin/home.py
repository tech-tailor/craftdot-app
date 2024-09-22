#!/usr/bin/python3
"""flask user account for craftdot"""



from flask import flash, Blueprint, render_template, request, abort,  make_response, current_app as app, send_from_directory, jsonify
from datetime import datetime
from flask_login import current_user, login_required
from frontend.loginmodel import User
import requests
from werkzeug.utils import secure_filename
import os



admin_bp = Blueprint("admin", __name__, subdomain='my-admin')


@admin_bp.route('/', methods=["GET"])
def home():
    return render_template('admin/home.html')

