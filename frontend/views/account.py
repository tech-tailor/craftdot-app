#!/usr/bin/python3
"""flask user account for craftdot"""



from flask import flash, Blueprint, render_template, request, abort, make_response, current_app as app, send_from_directory, jsonify, redirect, url_for
from datetime import datetime
from flask_login import current_user, login_required
from frontend.loginmodel import User
import requests
from werkzeug.utils import secure_filename
import os

account_bp = Blueprint("account", __name__, url_prefix='/account')


@account_bp.route('/profile', methods=["GET", "PUT"])
@login_required
def profile():
    """user profiles algo"""

    # Update user profile
    if request.method == 'PUT':
        # Get form data and user id
        user_update_form = request.form.to_dict()
        user_id = current_user.id
        # Save file to the user profile file and path to database
        filename = None
        if 'profile_picture' in request.files:
            print('yes')
            artisan_img = request.files['profile_picture']
            s_filename = secure_filename(artisan_img.filename)
            filename = f'{user_id}_{s_filename}'
            print(filename)
            directory = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            filepath = os.path.join(directory, filename)
            artisan_img.save(filepath)

        # call the update API with the data
        update_url = f'http://127.0.0.1:8000/api/v1/users/{user_id}'
        headers = {
            'Content-Type': "application/json"
        }
        data = user_update_form

        # Add profile_picture file to the user data to be updated
        profile_picture = {'profile_picture': filename}
        data.update(profile_picture)
        print('data....sfddsf....', data)
        r = requests.put(update_url, json=data, headers=headers)
        if r.status_code == 200:
            new_user_details = r.json()
            flash('You have succesfully updated your details', 'success')
            print(new_user_details)
            response = {
                'status_code': r.status_code,
                'content': new_user_details
            }
        

        else:
            response = {
                'status_code': r.status_code,
                'content': f"{r.content}"
            }
            
        #print('response', response)
        return response
                

    else:
        
        # Get user id
        user_id = current_user.id
        user_url = f"http://127.0.0.1:8000/api/v1/users/{user_id}"
        artisan_url = f"http://127.0.0.1:8000/api/v1/artisans/user_id/{user_id}"
        response = requests.get(user_url)
        if response.status_code == 200:
            user_data = response.json()
        else:
            user_data = None

        # Get artisan data
        response = requests.get(artisan_url)
        if response.status_code == 200:
            artisan_data = response.json()
        else:
            artisan_data = None
        
        if user_data['first_name'] == "" or user_data['last_name'] == "" or user_data['first_name'] is None or user_data['last_name'] is None:
                    print('about to redirect')
                    flash('You are yet to fill your name', 'info')
                    return redirect(url_for('account.update_name'))


        return render_template(
            'account/profile.html',
            user_data=user_data,
            artisan_data=artisan_data,
        )

@account_bp.route('/password')
@login_required
def change_password():
    """ Change user password"""
    return render_template(
        'account/change_password.html',
    )

@account_bp.route('/my-tasks')
@login_required
def my_tasks():
    """ Change user password"""
    return render_template(
        'account/my_tasks.html',
    )

@account_bp.route('/notification')
@login_required
def notification():
    """ Change user password"""
    return render_template(
        'account/notification.html',
    )

@account_bp.route('/profile/update', methods=["GET", "PUT"])
@login_required
def update_account():
    """ Update User details"""
            
    return render_template(
        'account/profile.html',
    )

#sample test to create artisan
@account_bp.route('/create', methods=['GET', 'POST'])
def create_artisan():
    """logics for the home page"""
    if request.method == 'POST':

        # Create artisans from the form data

        form_data = request.form.to_dict()
        #name = form_data['name']
        #skill = form_data['skill']
        #availability = form_data['availability']
        url = 'http://127.0.0.1:8000/api/v1/artisans'
       
        headers = {
            'Content-Type': 'application/json',
        }

        r = requests.post(url, json=form_data, headers=headers)
        if r.status_code == 201:
            flash('Artisan created successfully', 'success')
        else:
            flash('Failed to create artisan', 'danger')
        return render_template(
        'account/create_artisan.html',
        )
    
    if request.method == 'GET':
        service_url = 'http://127.0.0.1:8000/api/v1/services'
        # return all services data
        r = requests.get(service_url)
        if r.status_code == 200:
            services = r.json()
            print(services)
        else:
            services = None

        return render_template(
        'account/create_artisan.html',
        services=services
        )

@account_bp.route('/serve_image', methods=["GET"])
def serve_image():
    """Serve user profile picture"""
    print('wants to sand image')
    print(dir(current_user))
    user_id = current_user.id
    filename = "aea6a0a8-5da5-4edd-aac8-fc78588da437_asdfg.jpg"
    print('The User ID', user_id)
    try:
        directory = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
        print('send from directory', send_from_directory(directory, filename))
        return send_from_directory(directory, filename), 200
    
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404


@account_bp.route('/update_name', methods=["GET", "PUT"])
@login_required
def update_name():
    """ fresly enter User details"""

    if request.method == 'PUT':
        # Get the names on the form 
        form_data = request.form.to_dict()
        print(form_data)
        first_name = form_data['first_name']
        last_name = form_data['last_name']
        user_id = current_user.id
        # call the update API with the data
        update_url = f'http://127.0.0.1:8000/api/v1/users/{user_id}'
        headers = {
            'Content-Type': "application/json"
        }
        data = form_data
        r = requests.put(update_url, json=data, headers=headers)
        if r.status_code == 200:
            #new_user_details = r.json()
            flash('You have succesfully updated your name', 'success')
            response = {
                'status_code': r.status_code,      
            }
    
        else:
            response = {
                'status_code': r.status_code,
            }
        return response
    
    else:
        return render_template(
            'account/form_name.html',
        )
    
   