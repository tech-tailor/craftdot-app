#!/usr/bin/python3
"""flask user account for craftdot"""



from flask import flash, Blueprint, render_template, request, abort,make_response, current_app as app, send_from_directory, jsonify, flash, redirect, url_for
from datetime import datetime
from flask_login import current_user, login_required
from frontend.loginmodel import User
import requests
from werkzeug.utils import secure_filename
import os
from frontend.utils import allowed_file




admin_create_bp = Blueprint("admin_create", __name__,  subdomain='my-admin')


@admin_create_bp.route('/create-service', methods=["GET", "POST"])
def create_service():
    """ Create service type"""

    if request.method == "POST":
        # Get form details
        form_data = request.form.to_dict()
        service_name = form_data['name']
        data_class = 'Service'
        # Validate if service name is inputed
        if service_name is None or service_name == '':
            flash('Service name is required', 'error')
            return redirect(request.url)
        # Validate if picture
        if 'service_picture' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['service_picture']
        service_icon = request.files['service_icon']
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No service picture, please select a picture', 'error')
            return redirect(request.url)
        if service_icon.filename == '':
            flash('No service icon, please select an icon', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # Create the picture path for the service
            path = os.path.join(app.config['UPLOAD_FOLDER'], data_class, 'service_pictures')
            # Make sure these directories exist, else create them
            os.makedirs(path, exist_ok=True)
            # Save the file to the directory
            file.save(os.path.join(path, filename))
            # Append the picture file to the form dict data
            form_data['service_picture'] = filename
        else:
            flash('Invalid file')

        if service_icon and allowed_file(service_icon.filename):
            icon_name = secure_filename(service_icon.filename)
            
            # Create the picture path for the service
            path = os.path.join(app.config['UPLOAD_FOLDER'], data_class, 'service_icons')
            # Make sure these directories exist, else create them
            os.makedirs(path, exist_ok=True)
            # Save the file to the dirctory
            service_icon.save(os.path.join(path, icon_name))
            # Append the picture file to the form dict data
            form_data['service_icon'] = icon_name
        else:
            flash('Invalid icon')

        # validate double service name
        name = form_data['name']
        url = f'http://127.0.0.1:8000/api/v1/services/name/{name}'
        resp = requests.get(url)
        if resp.status_code == 200:
            service = resp.json()
            if service:
                flash(f'{name} already exists, create new service', 'error')
                return redirect(request.url)
            
        # Create service
        service_url = f'http://127.0.0.1:8000/api/v1/services'
        data = form_data
        headers = {
            'contentType': 'application/json'
        }
        print('data before saving', form_data)
        resp = requests.post(service_url, json=data, headers=headers)
        if resp.status_code == 201:
            flash('Service succesfully created', 'success')
        else:
            flash('An error occured creating this service', 'error')
            return redirect(request.url)
    return render_template('admin/create_service.html')


@admin_create_bp.route('/create-subservice', methods=["GET", "POST"])
def create_subservice():
    """ Create sub service type"""

    if request.method == "POST":
        # Get form details
        form_data = request.form.to_dict()
        service_name = form_data['name']
        # Append list to the form
        data_class = 'SubService'
        # Validate if subservice name is inputed
        if service_name is None or service_name == '':
            flash('Service name is required', 'error')
            return redirect(request.url)
        # Validate if picture
        if 'subservice_picture' not in request.files:
            flash('No file part')
            return redirect(request.url)
        subservice_picture = request.files['subservice_picture']
        # If user does not select file, browser also
        # submit an empty part without filename
        if subservice_picture.filename == '':
            flash('No subservice picture, please select a picture', 'error')
            return redirect(request.url)
        if subservice_picture and allowed_file(subservice_picture.filename):
            filename = secure_filename(subservice_picture.filename)
            
            # Create the picture path for the service
            path = os.path.join(app.config['UPLOAD_FOLDER'], data_class, 'pictures')
            # Make sure these directories exist, else create them
            os.makedirs(path, exist_ok=True)
            # Save the file to the directory
            subservice_picture.save(os.path.join(path, filename))
            # Append the picture file to the form dict data
            form_data['picture'] = filename
        else:
            flash('Invalid file')

        # validate double service name
        name = form_data['name']
        url = f'http://127.0.0.1:8000/api/v1/subservices/name/{name}'
        resp = requests.get(url)
        if resp.status_code == 200:
            service = resp.json()
            if service:
                flash(f'{name} already exists, create new service', 'error')
                return redirect(request.url)
        # Create service
        service_url = f'http://127.0.0.1:8000/api/v1/subservices'
        data = form_data
        headers = {
            'contentType': 'application/json'
        }
        print('data before saving subservice', form_data)
        resp = requests.post(service_url, json=data, headers=headers)
        if resp.status_code == 201:
            flash('Subservice succesfully created', 'success')
        else:
            flash(f'An error occured creating this subservice {resp.status_code}', 'error')
            return redirect(request.url)
        
    # Return major services available in the database when method is GET
    service_url = f'http://127.0.0.1:8000/api/v1/services'
    resp = requests.get(service_url)
    if resp.status_code == 200:
        services = resp.json()
        
    else:
        services = None
    return render_template(
        'admin/create_subservice.html',
        services=services,
        )



@admin_create_bp.route('/files/<service_id>', methods=['GET'])
def serve_file(service_id):
    """ serve retrieve file path from database """

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