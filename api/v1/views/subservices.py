#!/usr/bin/python3
""" objects that handle all default RestFul API actions for subservices """
from models.subservice import SubService
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
#from flasgger.utils import swag_from


@app_views.route('/subservices', methods=['GET'], strict_slashes=False)
#@swag_from('documentation/subservice/all_subservices.yml')
def get_subservices():
    """Retrieves the list of all subservices"""
    all_subservices = storage.all(SubService).values()
    subservice_list = []
    for subservice in all_subservices:
        subservice_list.append(subservice.to_dict())
    return subservice_list

@app_views.route('/subservices/<subservice_id>', methods=['GET'], strict_slashes=False)
#@swag_from('documentation/subservice/get_subservice.yml', methods=['GET'])
def get_subservice(subservice_id):
    """ Retrieves a single subservice """
    subservice = storage.get(SubService, subservice_id)
    if not subservice:
        abort(404)
    
    return jsonify(subservice.to_dict())
    

@app_views.route('/subservices/name/<name>', methods=['GET'], strict_slashes=False)
#@swag_from('documentation/subservice/get_subservice_by_name.yml', methods=['GET'])
def get_subservice_by_name(name):
    """ Retrieves a single subservice with name """
    subservice = storage.get_s(name)
    if not subservice:
        abort(404)
    
    return jsonify(subservice.to_dict())

@app_views.route('/subservices/<subservice_id>', methods=['DELETE'],
                 strict_slashes=False)
#@swag_from('documentation/subservice/delete_subservice.yml', methods=['DELETE'])
def delete_subservice(subservice_id):
    """
    Deletes a subservice Object
    """

    subservice = storage.get(SubService, subservice_id)

    if not subservice:
        abort(404)

    storage.delete(subservice)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/subservices', methods=['POST'], strict_slashes=False)
#@swag_from('documentation/subservice/post_subservice.yml', methods=['POST'])
def post_subservice():
    """
    Creates a subservice
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")
    if 'description' not in data:
        abort(400, description="Missing description")

    
    instance = SubService(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/subservices/<subservice_id>', methods=['PUT'], strict_slashes=False)
#@swag_from('documentation/subservice/put_subservice.yml', methods=['PUT'])
def put_subservice(subservice_id):
    """
    Updates a subservice
    """
    subservice = storage.get(SubService, subservice_id)

    if not subservice:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(subservice, key, value)
    storage.save()
    return make_response(jsonify(subservice.to_dict()), 200)