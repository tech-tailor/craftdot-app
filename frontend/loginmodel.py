from flask_login import UserMixin
from flask import request
import requests


class User(UserMixin):
    """ User class for Flask-Login"""
    def __init__(self, user_data):
        self.id = user_data.get('id')
        self.phone_number = user_data.get('phone_number')

    @staticmethod
    def get(user_id):
        # Make an API call to retrieve user data
        api_url = f"http://127.0.0.1:8000/api/v1/users/{user_id}"
        response = requests.get(api_url)
        if response.status_code == 200:
            user_data = response.json()
            return User(user_data)
        return None
        

    '''
    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        # Implement authentication logic (e.g., verify user credentials)
        return True

    def is_active(self):
        # Implement activation logic (e.g., check if user account is active)
        return True

    def is_anonymous(self):
        # Implement anonymous user logic
        return False
    '''