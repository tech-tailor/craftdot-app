#!/usr/bin/python3
""" Utiltiy fuctions that can be used"""

import random
from api.v1.config import EXPIRATION_TIME, SECRET_KEY
import datetime
import jwt

def generate_code(phone_number):
    """ Generates a random code """
    num = random.randint(100000, 999999)
    print(phone_number, num)

    return num



def generate_token(phone_number):
    """Generate user token with the phone number"""



    num = generate_code('phone_number')

    # Generate the jwt with phone number and the token
    token_payload = {
        'phone_number': phone_number,
        'otp': num,
        'exp': datetime.datetime.utcnow() + EXPIRATION_TIME
    }

    token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')
    return token