#!/usr/bin/python3
""" Utiltiy fuctions that can be used"""

from flask import current_app as app, send_file, send_from_directory
import random
import datetime
import jwt
from flask_mail import Message
from frontend.app import mail
import requests
import json
import os


def tokenized_otp(phone_number=None, email=None, password=None):
    """Generate jwt token with the phone number or email for authentication"""
    
    EXPIRATION_TIME = datetime.timedelta(minutes=10)
    SECRET_KEY = app.config['SECRET_KEY']

    otp = random.randint(100000, 999999)

    # Generate the jwt with phone number and the token
    token_payload = {
        'phone_number': phone_number,
        'email': email,
        'password': password,
        'otp': otp,
        'exp': datetime.datetime.utcnow() + EXPIRATION_TIME
    }
    try:
        token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')
        result = {
            'token_id': token,
            'otp': otp,
        }
        return result
    except Exception as e:
        return e

def untokenize_otp(token_id):
    """ Uncouple the data in the token """

    SECRET_KEY = app.config['SECRET_KEY']


    try:
        payload = jwt.decode(token_id, SECRET_KEY, algorithms='HS256')
        return payload
    except Exception as e:
        return e

def get_percent_val(value, percent):
    """ Return the percentage of any value"""

    r = (percent * value) / 100
    res = round(r)
    
    # return the rounded value of the given percentage
    return res 

def send_mail(message, recipients, subject):
    """ This sends mail"""

    msg = Message(
        subject=subject,
        recipients=[recipients]
    )
    msg.body = message
    try:
        print('about to send mail')
        mail.connect()
        res = mail.send(msg)
        print('mail sent')
        return res
    except Exception as e:
        print('Error', e)
        res = e
    return res

    

def send_phone_text(message, recipients, subject):
    """ This sends mail"""

    pass



def send_otp(phone_number):
    try:
        """ Send OTP to the user with the termii API"""
        BASE_URL = 'https://v3.api.termii.com'
        url = f"{BASE_URL}/api/sms/otp/generate"
        api_key = 'TLdlajiPTQEJYsjgFqEYOQxMcQhGFtMTrCUhfbOvBdhRDLsmRlfORuufLQMHhP'
        payload = {
            "api_key": api_key,
                "pin_type": "NUMERIC",
                "phone_number": phone_number,
                "pin_attempts": 3,
                "pin_time_to_live": 10,
                "pin_length": 6
        }
        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.post(url, headers=headers, json=payload)
        return json.loads(response.text)
    except Exception as e:
        print('Error occur with termii usage', e)

def verify_otp(pin_id, otp):
    """ Verify OTP with the termii API"""

    url = "https://BASE_URL/api/sms/otp/verify"
    api_key = 'TLdlajiPTQEJYsjgFqEYOQxMcQhGFtMTrCUhfbOvBdhRDLsmRlfORuufLQMHhP'
    payload = {
            "api_key": api_key,
            "pin_id": pin_id,
            "pin": otp,
        }
    headers = {
    'Content-Type': 'application/json',
    }
    response = requests.post(url, headers=headers, json=payload)
    print(response.text)
    return response.text

def allowed_file(filename):
    """ Check if the file is allowed"""

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


#@admin_create_bp.route('/files/<service_id>', methods=['GET'])
def serve_file(service_id):
    """ derve retrieve file path from database """

    # Get file from database
    
    service_url = f'http://127.0.0.1:8000/api/v1/services/{service_id}'
    
    resp = requests.get(service_url)
    if resp.status_code == 200:
        print()
        print()
        service_data = resp.json()
        service_name = service_data['name']
        service_picture = service_data['service_picture']

        if service_picture == None or service_picture == "":
            service_picture = "tailor.jpeg"
            service_path = os.path.join('/frontend', 'static', 'images')
            #print('file_path when NO file dey', service_path)
            full_path = os.path.join(service_path, service_picture)
            #print('FULL PATH with NO file', full_path)
            try:
                return send_from_directory(service_path, service_picture)
            except Exception as e:
                print('send_directory error with NO service picture...', e)
            
        else:
            # Construct file path
            service_path = os.path.join(app.config['UPLOAD_FOLDER'], 'service_pictures', service_name)
            #print('file_path when file dey', service_path)
            full_path = os.path.join(service_path, service_picture)
            #print('FULL PATH with file', full_path)

            try:
                return send_from_directory(service_path, service_picture)
            except Exception as e:
                print('send_directory error with service picture...', e)
    else:
        return 'error'


def serve_file(api_url, filename):
    """ derve retrieve file path from database """

    # Get file from database
    
    service_url = api_url
    
    resp = requests.get(service_url)
    if resp.status_code == 200:
        print()
        print()
        service_data = resp.json()
        name = service_data['name']
        file = service_data['filename']

    
        # Construct file path
        service_path = os.path.join(app.config['UPLOAD_FOLDER'], 'service_pictures', service_name)
        #print('file_path when file dey', service_path)
        full_path = os.path.join(service_path, service_picture)
        #print('FULL PATH with file', full_path)

        try:
            return send_from_directory(service_path, service_picture)
        except Exception as e:
            print('send_directory error with service picture...', e)
    else:
        return 'error'