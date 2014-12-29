import os
class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']

class ProductionConfig(Config):
    DEBUG = True
    DEVELOPMENT = True   

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
