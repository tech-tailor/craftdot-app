#!/usr/bin/python3
""" objects that handle all default RestFul API actions for verify """
from api.v1.config import EXPIRATION_TIME, SECRET_KEY
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from api.v1.utils import generate_code
import datetime
import jwt
#from flasgger.utils import swag_from


@app_views.route('/generate/token', methods=['POST'], strict_slashes=False)
#@swag_from('documentation/confirm/all_verify.yml')
def generate_token():
    """send verification number"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()

    if 'phone_number' not in data:
        abort(400, description="Missing phone number")
    if 'password' not in data:
        abort(400, description="Missing password")

    # Get user phonenumber and password
    phone_number = data.get('phone_number')
    password = data.get('password')

    # check if user exist
    user = storage.get_user_with_phone_no(phone_number)
    if user:
        abort(400, description="User already exist")

    # Generate the verification code/otp
    num = generate_code(data.get('phone_number'))

    # Generate the jwt with phone number and the token
    token_payload = {
        'phone_number': phone_number,
        'password': password,
        'otp': num,
        'exp': datetime.datetime.utcnow() + EXPIRATION_TIME
    }

    token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')
    return make_response(jsonify(token), 200)

    
@app_views.route('/verify/otp', methods=['POST'], strict_slashes=False)
#@swag_from('documentation/confirm/get_confirm.yml', methods=['GET'])
def verify_code():
    """ confirm the otp and jwt """
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()

    if 'token' not in data:
        abort(400, description="Missing token")
    if 'otp' not in data:
        abort(400, description="Missing otp")
    
    # Get the token and verification code
    token = data.get('token')
    otp = data.get('otp')

    # Convert the otp to int
    try:
        otp = int(otp)
    except Exception:
        abort(400, description="Invalid OTP")


    # Decode the token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
    except jwt.ExpiredSignatureError:
        abort(400, description="Token expired")
    except jwt.InvalidTokenError:
        abort(400, description="Invalid token")
    if payload['otp'] != otp:
        abort(400, description="Invalid OTP")
    
    return make_response(jsonify(True), 200)
    
