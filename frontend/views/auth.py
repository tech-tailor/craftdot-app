#!/usr/bin/python3
"""flask authentication for craftdot"""

from flask import flash, Blueprint, current_app, jsonify, render_template, abort, request, redirect, url_for, make_response
import requests
from flask_login import login_user, logout_user, login_required, current_user
from frontend.loginmodel import User
from frontend.utils import send_mail, send_phone_text, tokenized_otp, untokenize_otp
import datetime
import jwt
from frontend import utils


auth_bp = Blueprint("auth", __name__, url_prefix='/auth')



@auth_bp.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """logics for the home page"""


    if request.method == 'POST':
        # Get the login data converted to dict
        login_data = request.form.to_dict()
        # Get Phone number and password
        phone_number = login_data['phone_number']
        password = login_data['password']
        email = login_data['email']

        # When user login with email
        if email:
            #get the user object with phone number
            url = f'http://127.0.0.1:8000/api/v1/users/email/{email}'
            response = requests.get(url)
            if response.status_code == 200:
                user_data = response.json()
                # Chech if password is correct
                passwd_url = f'http://127.0.0.1:8000/api/v1/check_password/{user_data["id"]}/{password}'
                resp = requests.get(passwd_url)
                if resp.status_code != 200:
                    flash('Invalid login details', 'error')
                    return redirect(url_for('auth.login'))
                passwd_resp = resp.json()
                if user_data and passwd_resp != True:
                    flash('Invalid login details', 'error')
                    return redirect(url_for('auth.login'))
                user = User(user_data)
                login_user(user)
                # After user is aunthenticated, check if the user form is filled
                if user_data['first_name'] == "" or user_data['last_name'] == "" or user_data['first_name'] is None or user_data['last_name'] is None:
                    return redirect(url_for('account.update_name'))
                flash('you have succesfully login', 'success')
                next = request.args.get('next')
                return redirect(next or url_for('service.booking'))
            elif response.status_code == 404:
                flash("User not found", "error")
                return redirect(url_for('auth.login'))

            else:
                flash("Error logging in", 'error')
                return redirect(url_for('auth.login'))
        
        # When user login with phone number
        elif phone_number:
            #get the user object with phone number
            url = f'http://127.0.0.1:8000/api/v1/users/number/{phone_number}'
            response = requests.get(url)
            if response.status_code == 200:
                user_data = response.json()
                print('daattaaa', user_data)
                # Chech if password is correct
                passwd_url = f'http://127.0.0.1:8000/api/v1/check_password/{user_data["id"]}/{password}'
                resp = requests.get(passwd_url)
                if resp.status_code != 200:
                    flash('Invalid login details', 'error')
                    return redirect(url_for('auth.login'))
                passwd_resp = resp.json()
                if user_data and passwd_resp != True:
                    flash('Invalid login details', 'error')
                    return redirect(url_for('auth.login'))
                user = User(user_data)
                login_user(user)
                # After user is aunthenticated, check if the user form is filled
                if user_data['first_name'] == "" or user_data['last_name'] == "" or user_data['first_name'] is None or user_data['last_name'] is None:
                    print('about to redirect')
                    return redirect(url_for('account.update_name'))
                flash('you have succesfully login', 'success')
                next = request.args.get('next')
                return redirect(next or url_for('service.booking'))
            elif response.status_code == 404:
                flash("User not found", "error")
                return redirect(url_for('auth.login'))

            else:
                flash("Error logging in", 'error')
                return redirect(url_for('auth.login'))

    else:
        if current_user.is_authenticated:
            # send flash msg when user is login
            flash("You are logged in", 'success')
            next = request.args.get('next')
            return redirect(next or url_for('main.home'))
        else:
            # send flash msg when user is not login
            #flash("Please log in", "info")
            return render_template('auth/login.html')

            
    
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """ View to register user"""

    try:
        if request.method == 'POST':
            data = request.get_json()

            # Get Phone number and password
            phone_number = data.get('phone_number')
            password = data.get('password')
            email = data.get('email')

            # Use this when user register with email
            if email:
                #get the user object with email
                url = f'http://127.0.0.1:8000/api/v1/users/email/{email}'
                response = requests.get(url)
                if response.status_code == 200:
                    user = response.json()
                    print(user)
                    # Check if user exist
                    if user:
                        return jsonify('User already exist'), 409 
                elif response.status_code == 404:
                    # Tokenize the otp with jwt
                    token = tokenized_otp(email=email, password=password)
                    print(token)
                    otp = token['otp']
                    token = token['token_id']
                    
                    # send token to my email for test, it will be the user phone number
                    message = f"This is your Craftdot OTP {otp} and it will expire in 10 minutes. Do not share with anyone"
                    send_mail(message, recipients=email, subject='OTP')
            
                    return jsonify(token), 200
                else:
                    print('unknown error')
                    return('unknown error')
            
            # Use this when user register with phone number
            elif phone_number:
                #get the user object with phone number
                url = f'http://127.0.0.1:8000/api/v1/users/number/{phone_number}'
                response = requests.get(url)
                if response.status_code == 200:
                    user = response.json()
                    # Check if user exist
                    if user:
                        return jsonify('User already exist'), 409 
                else:
                    # Tokenize the otp with jwt
                    token = tokenized_otp(phone_number=phone_number, password=password)
                    print(token)
                    otp = token['otp']
                    token = token['token_id']
                    
                    # send token to my email for test, it will be the user phone number
                    message = f"This is your Craftdot OTP {otp} and it will expire in 10 minutes. Do not share with anyone"

                    send_phone_text(message, recipients=phone_number, subject='OTP')
            
                    return jsonify(token), 200
        elif request.method == 'GET':
            return render_template('auth/register.html')
    except Exception as e:
        return jsonify('Error with registration, please try later'), 400    #render_template('auth/register.html')

    

    
@auth_bp.route('/verify/otp', methods=['POST'], strict_slashes=False)
def verify_code():
    """ confirm the jwt token"""

    SECRET_KEY = current_app.config['SECRET_KEY']
    data = request.get_json()

    if 'token' not in data:
        abort(400, description="Missing token")
        #return jsonify('Missing token', 200)
    if 'otp' not in data:
        abort(400, description="Missing OTP")
        #return jsonify('Missing OTP', 200)
    
    # Get the token and verification code
    token = data.get('token')
    otp = data.get('otp')

    # Convert the otp to int
    try:
        otp = int(otp)
    except Exception:
        #abort(400, description="Invalid OTP")
        return jsonify('Invalid OTP'), 400


    # Decode the token
    try:
        payload = untokenize_otp(token)
        if payload['otp'] != otp:
            flash('Invalid OTP, try again', 'error')
            return jsonify('Invalid OTP'), 400
        return jsonify('OTP verified!'), 200
    except jwt.ExpiredSignatureError:
        return jsonify('OTP Expired'), 400
    except jwt.InvalidTokenError:
        return jsonify('Invalid cOTP'), 400
    

@auth_bp.route('/create-user', methods=['POST'])
def create_user():
    """ Create user after verification """

    data = request.get_json()

    # Get OTP and token
    token = data.get('token')

    # Confirm the jwt again
    try:
        payload = untokenize_otp(token)
        phone_number = payload['phone_number']
        password = payload['password']
        email = payload['email']
    except Exception:
        return jsonify('Invalid token'), 400
   
    print('this password', password)
    print('email oooo', email)
    if phone_number:
        #get the user object with phone number
        url = f'http://127.0.0.1:8000/api/v1/users/number/{phone_number}'
        response = requests.get(url)
        if response.status_code == 200:
            user = response.json()
            # Check if user exist
            if user:
                flash('User already exist', 'error') # flash can be info, success or error
                abort(400)
        else:
            # Register User
            print('about to register')
            register_url = f'http://127.0.0.1:8000/api/v1/users'
            data = {
                'phone_number': phone_number,
                'password': password,
            }

            headers = {
                'contentType': 'application/json'
            }
            response = requests.post(register_url, json=data, headers=headers)
            if response.status_code == 200:
                flash('Registration succesful, please login', 'success')
                return jsonify('User created, you will be redirected to the login page'), 200
            else:
                flash('Some error, user not created. Try again', 'error')
                return jsonify('Some error, user not created. Try again'), 400
    
    elif email:
        #get the user object with email
        print('na email ooo', email)
        url = f'http://127.0.0.1:8000/api/v1/users/email/{email}'
        response = requests.get(url)
        if response.status_code == 200:
            user = response.json()
            # Check if user exist
            if user:
                flash('User already exist', 'error') # flash can be info, success or error
                abort(400)
        else:
            # Register User
            print('about to register with email')
            print('email..........', email)
            print('password..........', password)
            register_url = f'http://127.0.0.1:8000/api/v1/users'
            data = {
                'email': email,
                'password': password,
            }

            headers = {
                'contentType': 'application/json'
            }
            response = requests.post(register_url, json=data, headers=headers)
            print(response.content)
            if response.status_code == 200:
                flash('Registration succesful, please login', 'success')
                return jsonify('User created, you will be redirected to the login page'), 200
            else:
                flash(f'Some error, user not created. Try again, {response.status_code}', 'error')
                return jsonify('Some error, user not created. Try again'), 400  

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out', 'success')
    return redirect(url_for('main.home'))



@auth_bp.route('/become-a-craftdotter', methods=['GET', 'POST'])
def register_artisan():
    """ View to register artisans"""

    try:
        if request.method == 'POST':
            data = request.get_json()

            # Get email and password
            password = data.get('password')
            email = data.get('email')

            
            #get the user object with email
            url = f'http://127.0.0.1:8000/api/v1/users/email/{email}'
            response = requests.get(url)
            if response.status_code == 200:
                user = response.json()
                print(user)
                # Check if user exist
                if user:
                    return jsonify('User already exist'), 409 
            elif response.status_code == 404:
                # Tokenize the otp with jwt
                token = tokenized_otp(email=email, password=password)
                print(token)
                otp = token['otp']
                token = token['token_id']
                
                # send token to my email for test, it will be the user phone number
                message = f"This is your Craftdot OTP {otp} and it will expire in 10 minutes. Do not share with anyone"
                send_mail(message, recipients=email, subject='OTP')
        
                return jsonify(token), 200
            else:
                print('unknown error')
                return('unknown error')
            
            
        elif request.method == 'GET':
            return render_template('auth/register_artisan.html')
    except Exception as e:
        return jsonify('Error with registration, please try later'), 400    #render_template('auth/register.html')

@auth_bp.route('/create-artisan', methods=['POST'])
def create_artisan():
    """ Create user after verification """

    data = request.get_json()

    # Get OTP and token
    token = data.get('token')

    # Confirm the jwt again
    try:
        payload = untokenize_otp(token)
        password = payload['password']
        email = payload['email']
    except Exception:
        return jsonify('Invalid token'), 400
   
    print('this password', password)
    print('email oooo', email)
    
    
    if email and password:
        #get the user object with email
        print('na email ooo', email)
        url = f'http://127.0.0.1:8000/api/v1/users/email/{email}'
        response = requests.get(url)
        if response.status_code == 200:
            user = response.json()
            # Check if user exist
            if user:
                flash('You are already a user, you want to convert to an artisan account', 'info') # flash can be info, success or error
                #abort(409)
        else:
            # Register User first, an artisan is firstly a user
            print('about to register with email')
            print('email..........', email)
            print('password..........', password)
            artisan_url = f'http://127.0.0.1:8000/api/v1/artisans'
            data = {
                'email': email,
                'password': password,
            }

            headers = {
                'contentType': 'application/json'
            }
            response = requests.post(artisan_url, json=data, headers=headers)
            print(response.content)
            if response.status_code == 200:  
                flash('Registration succesful, please login', 'success')
                return jsonify('Artisan created, you will be redirected to the login page'), 200
            else:
                flash(f'Some error, your account was not created. Try again, {response.status_code}', 'error')
                return jsonify('Some error, your account was not created. Try again'), 400 