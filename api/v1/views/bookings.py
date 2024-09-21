#!/usr/bin/python3
""" objects that handle all default RestFul API actions for bookings """
from models.booking import Booking
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
#from flasgger.utils import swag_from


@app_views.route('/bookings', methods=['GET'], strict_slashes=False)
#@swag_from('documentation/booking/all_bookings.yml')
def get_bookings():
    """Retrieves the list of all bookings"""
    all_bookings = storage.all(Booking).values()
    booking_list = []
    for booking in all_bookings:
        booking_list.append(booking.to_dict())
    return booking_list

@app_views.route('/bookings/<booking_id>', methods=['GET'], strict_slashes=False)
#@swag_from('documentation/booking/get_booking.yml', methods=['GET'])
def get_booking(booking_id):
    """ Retrieves a single booking """
    booking = storage.get(Booking, booking_id)
    if not booking:
        abort(404)
    
    return jsonify(booking.to_dict())

@app_views.route('/bookings/<booking_id>', methods=['DELETE'],
                 strict_slashes=False)
#@swag_from('documentation/booking/delete_booking.yml', methods=['DELETE'])
def delete_booking(booking_id):
    """
    Deletes a booking Object
    """

    booking = storage.get(Booking, booking_id)

    if not booking:
        abort(404)

    storage.delete(booking)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/bookings', methods=['POST'], strict_slashes=False)
#@swag_from('documentation/booking/post_booking.yml', methods=['POST'])
def post_booking():
    """
    Creates a booking
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    if 'service_id' not in data:
        abort(400, description="Missing service_id")
    if 'artisan_id' not in data:
        abort(400, description="Missing artisan_id")

    
    instance = Booking(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/bookings/<booking_id>', methods=['PUT'], strict_slashes=False)
#@swag_from('documentation/booking/put_booking.yml', methods=['PUT'])
def put_booking(booking_id):
    """
    Updates a booking
    """
    booking = storage.get(Booking, booking_id)

    if not booking:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(booking, key, value)
    storage.save()
    return make_response(jsonify(booking.to_dict()), 200)