#!/usr/bin/python3
""" objects that handle all default RestFul API actions for artisans """
from models.artisan import Artisan
from models.user import User
from models import storage
from api.v1.views import app_views
from sqlalchemy.exc import IntegrityError
from flask import abort, jsonify, make_response, request
#from flasgger.utils import swag_from

@app_views.route('/artisans', methods=['GET'], strict_slashes=False)
#@swag_from('documentation/artisan/all_artisans.yml')
def get_artisans():
    """Retrieves the list of all artisans"""
    all_artisans = storage.all(Artisan).values()
    artisan_list = []
    for artisan in all_artisans:
        artisan_list.append(artisan.to_dict())
    return artisan_list

@app_views.route('/artisans/<artisan_id>', methods=['GET'], strict_slashes=False)
#@swag_from('documentation/artisan/get_artisan.yml', methods=['GET'])
def get_artisan(artisan_id):
    """ Retrieves a single artisan """
    user = storage.get(Artisan, artisan_id)
    if not user:
        abort(404)
    
    return jsonify(user.to_dict())

@app_views.route('/artisans/user_id/<user_id>', methods=['GET'], strict_slashes=False)
#@swag_from('documentation/artisan/get_artisan_with_userid.yml', methods=['GET'])
def get_artisan_with_user_id(user_id):
    """ Retrieves a single artisan using user ID"""

    user = storage.get(User, user_id)
    if not user:
        abort(404)
    artisan = user.artisan
    if not artisan:
        abort(404)
    
    return jsonify(artisan.to_dict())


@app_views.route('/artisans', methods=['POST'], strict_slashes=False)
#@swag_from('documentation/artisan/post_artisan.yml', methods=['POST'])
def post_artisan():
    """
    Creates an artisan with a user id.
    every artisan is firstly a user
    """
    # Create user first

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()

    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")
    
    # Check if user already exists
    user = storage.get_user_with_email(data.get('email'))
    if user:
        # Check if artisan exist
        #user_data = storage.get(User, user.id)   # Get user data
        # Check if the user is an artisan
        artisan = (user.artisan) # Get artisan data from the user
        print('Artisan -------', artisan)
        if artisan:
            abort(400, description="Artisan already exists")
        # create artisan model instance when user already exist
        user.is_artisan = True
        artisan = Artisan(user_id=user.id, **data)
        #user.artisan_profile = artisan
        artisan.save()
        return make_response(jsonify(artisan.to_dict()), 201)
    else:
        # Create user instance
        user_instance = User(**data)
        
        user_instance.save()
        
        # Create artisan instance
        user_instance.is_artisan = True
        artisan_instance = Artisan(user_id=user_instance.id, **data)
        #artisan_instance.user = user_instance
        #user_instance.artisan_profile = artisan_instance
        artisan_instance.save()

        return  make_response(jsonify(artisan_instance.to_dict()), 201)

        
'''        
except IntegrityError as e:
    # Handle IntegrityError (e.g., user already exists in the database)
    abort(400, description="User already exists")
    

except AttributeError as e:
    # Handle AttributeError (e.g., if the JSON data is missing required fields)
    abort(400, description="Missing required attribute: " + str(e))

except Exception as e:
    # Handle other exceptions
    abort(500, description="Internal Server Error: " + str(e))
'''

@app_views.route('/artisans/<artisan_id>', methods=['DELETE'],
                 strict_slashes=False)
#@swag_from('documentation/artisan/delete_artisan.yml', methods=['DELETE'])
def delete_artisan(artisan_id):
    """
    Deletes an artisan Object
    """

    artisan = storage.get(Artisan, artisan_id)

    if not artisan:
        abort(404)

    storage.delete(artisan)
    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('/artisans/<artisan_id>', methods=['PUT'], strict_slashes=False)
#@swag_from('documentation/artisan/put_artisan.yml', methods=['PUT'])
def put_artisan(artisan_id):
    """
    Updates a user
    """
    artisan = storage.get(Artisan, artisan_id)

    if not artisan:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'email', 'phone_number', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(artisan, key, value)
    storage.save()
    return make_response(jsonify(artisan.to_dict()), 200)