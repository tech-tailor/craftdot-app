#!/usr/bin/python3
"""flask """

from flask import flash, Blueprint, render_template, request, redirect, url_for, current_app as app, send_from_directory
from datetime import datetime
import requests
import os


main_bp = Blueprint("main", __name__)

@main_bp.route('/')
def home():
    """logics for the home page"""
    
    # Get just few services to display in the home page
    service_url = f'http://127.0.0.1:8000/api/v1/services'
    
    resp = requests.get(service_url)
    if resp.status_code == 200:
        services = resp.json()
    else:
        services = None

    # Get all the subservices
    subservice_url = f'http://127.0.0.1:8000/api/v1/subservices'
    
    resp = requests.get(subservice_url)
    if resp.status_code == 200:
        subservices = resp.json()
    else:
        services = None
    
    
    return render_template(
        'main/home.html',
        services=services,
        subservices=subservices,
    )

@main_bp.route('/subservice/<service_id>')
def subservices(service_id):
    """logics for sub services related to a service"""

    service_url = f'http://127.0.0.1:8000/api/v1/service/subservices/{service_id}'
    
    resp = requests.get(service_url)
    if resp.status_code == 200:
        subservices = resp.json()
    else:
        subservices = None
    
    return subservices

@main_bp.route('/contact-us')
def contact_us():
    """logics for the contact us page"""
    
    return render_template(
        'main/contact_us.html'
    )

@main_bp.route('/about-us')
def about_us():
    """logics for the about us page"""
    
    return render_template(
        'main/about_us.html'
    )

@main_bp.route('/privacy-policy')
def privacy_policy():
    """logics for the about us page"""
    
    return render_template(
        'main/privacy_policy.html'
    )



@main_bp.route('/learn', defaults={'topic': None})
@main_bp.route('/learn/<string:topic>')
def learn(topic=None):
    """logics for the learning page"""

    if topic is None:
        return render_template(
            'main/learn.html'
        )
    else:
        temlate_path = f"learn/{topic}.html"
        try:
            return render_template(
                temlate_path
            )
        except:
            msg = "No such leaarning"
            return render_template(
                'main/learn.html',
                msg=msg
            )
        
@main_bp.route('/dashboard')
def dashboard():
    """logics for dashboard, it shows all services"""
    
    return render_template(
        'main/dashboard.html'
    )

@main_bp.route('/files/<service_id>/<file_name>', methods=['GET'])
def serve_file(service_id, file_name):
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
        service_icon = service_data['service_icon']
        data_class = service_data['__class__']
        if service_picture == file_name:
            # Construct file path
            service_path = os.path.join(app.config['UPLOAD_FOLDER'], data_class, 'service_pictures')
            #print('file_path when file dey', service_path)
            full_path = os.path.join(service_path, service_picture)
            #print('FULL PATH with file', full_path)

            try:
                return send_from_directory(service_path, service_picture)
            except Exception as e:
                print('send_directory error with service picture...', e)

        elif service_icon == file_name:
            print('service_icon', service_icon, 'file_name', file_name)
            # Construct file path
            service_path = os.path.join(app.config['UPLOAD_FOLDER'], data_class, 'service_icons')
            #print('file_path when file dey', service_path)
            full_path = os.path.join(service_path, service_picture)
            #print('FULL PATH with file', full_path)

            try:
                return send_from_directory(service_path, service_icon)
            except Exception as e:
                print('send_directory error with service picture...', e)
    else:
        return 'error'
