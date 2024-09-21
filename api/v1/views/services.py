#!/usr/bin/python3
""" objects that handle all default RestFul API actions for services """
from models.service import Service
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
#from flasgger.utils import swag_from


@app_views.route('/services', methods=['GET'], strict_slashes=False)
#@swag_from('documentation/service/all_services.yml')
def get_services():
    """Retrieves the list of all services"""
    all_services = storage.all(Service).values()
    service_list = []
    for service in all_services:
        service_list.append(service.to_dict())
    return service_list

@app_views.route('/services/<service_id>', methods=['GET'], strict_slashes=False)
#@swag_from('documentation/service/get_service.yml', methods=['GET'])
def get_service(service_id):
    """ Retrieves a single service """
    service = storage.get(Service, service_id)
    if not service:
        abort(404)
    
    return jsonify(service.to_dict())

@app_views.route('/service/subservices/<service_id>', methods=['GET'], strict_slashes=False)
#@swag_from('documentation/service/get_subservices_within_a_single_service.yml', methods=['GET'])
def get_subservices_within_a_service(service_id):
    """ Retrieves subservices within a single service """
    service = storage.get(Service, service_id)
    if not service:
        abort(404)

    subservices = service.subservices
    subservice_list = []
    for subservice in subservices:
        subservice_list.append(subservice.to_dict())
    

    return jsonify(subservice_list)

@app_views.route('/services/name/<name>', methods=['GET'], strict_slashes=False)
#@swag_from('documentation/service/get_service_by_name.yml', methods=['GET'])
def get_service_by_name(name):
    """ Retrieves a single service with name """
    service = storage.get_s(name)
    if not service:
        abort(404)
    
    return jsonify(service.to_dict())

@app_views.route('/services/<service_id>', methods=['DELETE'],
                 strict_slashes=False)
#@swag_from('documentation/service/delete_service.yml', methods=['DELETE'])
def delete_service(service_id):
    """
    Deletes a service Object
    """

    service = storage.get(Service, service_id)

    if not service:
        abort(404)

    storage.delete(service)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/services', methods=['POST'], strict_slashes=False)
#@swag_from('documentation/service/post_service.yml', methods=['POST'])
def post_service():
    """
    Creates a service
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")
    if 'description' not in data:
        abort(400, description="Missing description")

    
    instance = Service(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/services/<service_id>', methods=['PUT'], strict_slashes=False)
#@swag_from('documentation/service/put_service.yml', methods=['PUT'])
def put_service(service_id):
    """
    Updates a service
    """
    service = storage.get(Service, service_id)

    if not service:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(service, key, value)
    storage.save()
    return make_response(jsonify(service.to_dict()), 200)