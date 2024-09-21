#!/usr/bin/python3
""" objects that handle all default RestFul API actions for reviews """
from models.review import Review
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
#from flasgger.utils import swag_from


@app_views.route('/reviews', methods=['GET'], strict_slashes=False)
#@swag_from('documentation/review/all_reviews.yml')
def get_reviews():
    """Retrieves the list of all reviews"""
    all_reviews = storage.all(Review).values()
    review_list = []
    for review in all_reviews:
        review_list.append(review.to_dict())
    return review_list

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
#@swag_from('documentation/review/get_review.yml', methods=['GET'])
def get_review(review_id):
    """ Retrieves a single review """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
#@swag_from('documentation/review/delete_review.yml', methods=['DELETE'])
def delete_review(review_id):
    """
    Deletes a review Object
    """

    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/reviews', methods=['POST'], strict_slashes=False)
#@swag_from('documentation/review/post_review.yml', methods=['POST'])
def post_review():
    """
    Creates a review
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")
    if 'description' not in data:
        abort(400, description="Missing description")

    
    instance = Review(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
#@swag_from('documentation/review/put_review.yml', methods=['PUT'])
def put_review(review_id):
    """
    Updates a review
    """
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)