import os


class Config:
    SECRET_KEY = os.getenv('APP_SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = os.getenv('APP_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = 'redis'
    # CACHE_REDIS_HOST = os.getenv('CACHE_HOST')
    # CACHE_REDIS_PORT = os.getenv('CACHE_PORT')
    # CACHE_REDIS_PASSWORD = os.getenv('CACHE_PASSWORD')
    # CACHE_REDIS_DB = os.getenv('CACHE_DB')
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_URL = os.getenv('APP_CACHE_URI')

    MAIL_WORKERS = os.getenv('MAIL_WORKERS', 1)

    SERVER_NAME = os.environ.get('SERVER_NAME', 'localhost:8080')


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    WTF_CSRF_ENABLED = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False


def get_app_config(env: str):
    configs = {
        'development': 'config.DevelopmentConfig',
        'production': 'config.ProductionConfig',
        'testing': 'config.testingConfig',
    }
    return configs.get(env)
