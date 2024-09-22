import os
from dotenv import load_dotenv


# Load environment variables from .env file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """Base configuration"""
    SECRET_KEY =  os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'SimpleCache'  # Can be "memcached", "redis"
    CACHE_DEFAULT_TIMEOUT = os.getenv('CACHE_DEFAULT_TIMEOUT')
    RECAPTCHA_SECRET_KEY = os.getenv('RECAPTCHA_SECRET_KEY')
    RECAPTCHA_SITE_KEY = os.getenv('RECAPTCHA_SITE_KEY')
    UPLOAD_FOLDER = os.path.abspath('uploads')
    DEFAULT_PICTURE_FOLDER = os.path.abspath('default_pictures')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'ogundareakinniyi8@gmail.com'
    MAIL_PASSWORD =  os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Craftdot', 'info@craftdot.com.ng')
    
    

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SERVER_NAME = 'localhost:8001'
    MAIL_DEBUG = True


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'
  



class ProductionConfig(Config):
    """Production configuration"""
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        #'sqlite:///' + os.path.join(basedir, 'app.db')
    SERVER_NAME = 'craftdot.com.ng'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}