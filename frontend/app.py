#!/usr/bin/python3
""" Flask Application """
from dotenv import load_dotenv
import os
from frontend import create_app
from flask_login import LoginManager
from frontend.loginmodel import User
from flask import render_template
from flask_caching import Cache
from flask_socketio import SocketIO
from flask_mail import Mail

load_dotenv()
craftdot_env = os.getenv('CRAFTDOT_ENV')

#from flask_cors import CORS
#from flasgger import Swagger
#from flasgger.utils import swag_from

app = create_app(craftdot_env or 'production')  # or 'production', 'testing', etc.
#cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
cache = Cache(app)
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)
mail = Mail(app)

# Register Blueprint
from frontend.views.main import main_bp
from frontend.views.auth import auth_bp
from frontend.views.account import account_bp
from frontend.views.service import service_bp
from frontend.views.message import message_bp
from frontend.views.admin.home import admin_bp
from frontend.views.admin.create_service import admin_create_bp
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(account_bp)
app.register_blueprint(service_bp)
app.register_blueprint(message_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(admin_create_bp)
    

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return render_template("errors/404.html"), 404
