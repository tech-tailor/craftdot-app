#!/usr/bin/python3
""" Flask Application """
from api.v1.config import SECRET_KEY, EXPIRATION_TIME
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
import jwt
import datetime
#from flasgger import Swagger
#from flasgger.utils import swag_from


app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})





@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)

app.config['SWAGGER'] = {
    'title': 'CraftDot Restful API',
    'uiversion': 1
}

#Swagger(app)

