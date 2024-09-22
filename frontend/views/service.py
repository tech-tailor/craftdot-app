#!/usr/bin/python3
"""flask homepage for birthday celebration app"""

from flask import flash, Blueprint, render_template, request, redirect, jsonify, url_for, abort
from datetime import datetime
import requests
from frontend.app import cache
from flask import current_app as app
from flask_login import current_user, login_required
import json


service_bp = Blueprint("service", __name__, url_prefix="/services")

@service_bp.route('/')
@cache.cached(timeout=30)
def service():
    """logics for the home page"""

    service_url = f'http://127.0.0.1:8000/api/v1/services'
    r = requests.get(service_url)
    if r.status_code == 200:
        service = r.json()
        services = service

    else:
        services = None
    
    return render_template(
        'services/services.html',
        services=services,
    )
    

@service_bp.route('/booking')
@cache.cached(timeout=30)
def booking():
    """logics for booking details"""

    service_url = f'http://127.0.0.1:8000/api/v1/services'
    r = requests.get(service_url)
    if r.status_code == 200:
        service = r.json()
        services = service

    else:
        services = None
 
    return render_template(
        'services/booking.html',
        services=services,
    )


@service_bp.route('/booking/<string:service_id>')
@cache.cached(timeout=30)
def booking_detail(service_id):
    """logics for booking details"""
    # Get the name of the service
    r = requests.get(f'http://127.0.0.1:8000/api/v1/services/{service_id}')
    if r.status_code == 200:
        service = r.json()
        service_name = service['name']

    else:
        if r.status_code == 404:
            return abort(404)
        
    # Get all the states and LGAS
    with open('country_data/state.json', 'r') as f:
        all_state = json.load(f)
        states = []
        for state in all_state['geonames']:
            state_name = state['name'].split(" ")[0] # split and pick only state name
            # Append each state to alist
            states.append(state_name)
            # Arrange the states alphabetically
            states.sort()
    # Get all the LGAs
    with open('country_data/LGA.json', 'r') as f:
        all_LGA = json.load(f)
        LGAs = []
        for lga in all_LGA['geonames']:
            lga_name = lga['name']
            lga_state = lga['adminName1'].split(" ")[0]
            data = {
                'LGA': lga_name,
                'state': lga_state
            }
            LGAs.append(data)

        lga_data = {state: [] for state in states}

        for lga in LGAs:
            state = lga['state']
            lga_name = lga['LGA']
            if state in lga_data:
                lga_data[state].append(lga_name)
        lga_data=lga_data
            

    return render_template(
        'services/booking_details.html',
        service_name=service_name,
        service_id=service_id,
        states=states,
        lga_data=lga_data
    )


@service_bp.route('/booking/recommendation/<service_id>', methods=['GET', 'POST'], endpoint='booking_recommendation')
#@cache.cached(timeout=30)
def booking_recommendation(service_id):
    """logics for booking recommendation"""
    if request.method == 'POST':
        # Get form data
        user_task_details = request.form.to_dict()
        #Get service name
        r = requests.get(f'http://127.0.0.1:8000/api/v1/services/{service_id}')
        if r.status_code == 200:
            service = r.json()
            service_name = service['name']

        else:
            if r.status_code == 404:
                return abort(404)

        # Get all artisans before recommendation
        r = requests.get('http://127.0.0.1:8000/api/v1/artisans')
        if r.status_code == 200:
            all_artisans = r.json()

            # This is where the app algorithim lies, connect users to artisans based on location, ...
            # Merging artisans and users
            # List all artisans with the same service the user want
            artisans_with_similar_service = []
            artisans_user_data = []
            for artisan in all_artisans:
                if artisan['service_id'] == service_id:
                    artisans_with_similar_service.append(artisan)
                    # Get the artisan user datas using artisan user_id
                    artisan_user_id = artisan['user_id']
                    r = requests.get(f'http://127.0.0.1:8000/api/v1/users/{artisan_user_id}')
                    if r.status_code == 200:
                        artisan_user = r.json()
                        artisans_user_data.append(artisan_user)
                    else:
                        artisan_user = None

            artisans = artisans_with_similar_service
            artisans_user_data = artisans_user_data

            
        else:
            artisans = None
        artisans = artisans

        return render_template(
        'services/booking_recommendation.html',
        service_name=service_name,
        artisans=artisans,
        artisans_user_data = artisans_user_data,
        service_id=service_id,
        user_task_details=user_task_details
        )
    else:
        return redirect(url_for('service.booking'))


@service_bp.route('/booking/confirm/<service_id>',  methods=['GET', 'POST'])
@login_required
@cache.cached(timeout=30)
def booking_confirm(service_id):
    """logics for booking details"""

    # Get recaptcha site key
    recaptcha_site_key = app.config['RECAPTCHA_SITE_KEY']
    

    if request.method == 'POST':
        user_request = request.form.to_dict()
        booking = user_request

        # Get 10% of the booking fee
        booking_fee = float(booking['artisan_price'])
        ten_percent_booking_fee = booking_fee * 0.1

        # Total booking fee
        total_booking_fee = booking_fee + ten_percent_booking_fee

        return render_template(
            'services/booking_confirm.html',
            booking=booking,
            service_id=service_id,
            recaptcha_site_key=recaptcha_site_key,
            ten_percent_booking_fee=ten_percent_booking_fee,
            total_booking_fee=total_booking_fee,
        )
    
    else:
        return redirect(url_for('service.booking'))
    


@service_bp.route('/book/task',  methods=['GET', 'POST'])
@login_required
@cache.cached(timeout=30)
def book_task():
    """logics for booking details"""

    # Get recaptcha secret keys
    recaptcha_secret_key = app.config['RECAPTCHA_SECRET_KEY']
    # Get current user
    user_id=current_user.id

    print('Recapcha', recaptcha_secret_key)

    if request.method == 'POST':
        print('Recapcha', recaptcha_secret_key)
        recaptcha_response = request.form['g-recaptcha-response']
        data = {
            'secret': recaptcha_secret_key,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        if not result['success']:
            flash('Invalid recaptcha. Please try again', 'danger')
            #return redirect(url_for('service.booking'))
            return jsonify({'message': 'reCAPTCHA verification failed'}), 400
        
        # Get form data
        form_data = request.form.to_dict()
        # del recapcha key-value from the form data
        form_data.pop('g-recaptcha-response')
        # Add user_id to the form
        user_id = {'user_id': user_id}
        form_data.update(user_id)

        # Create Booking
        booking_url = 'http://127.0.0.1:8000/api/v1/bookings'
       
        headers = {
            'Content-Type': 'application/json',
        }

        r = requests.post(booking_url, json=form_data, headers=headers)
        if r.status_code == 201:
            response = r.json()
            
        else:
            response = {
                'code': r.status_code,
                'message': r.content
            }

        
        return render_template(
            'services/booking_success.html',
            result=result,
            response=response,
            d=form_data
        ) 
    else:
        return redirect(url_for('service.booking'))