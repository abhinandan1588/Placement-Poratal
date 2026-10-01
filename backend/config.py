import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE = os.path.join(BASE_DIR , "instance")
os.makedirs(INSTANCE , exist_ok=True)
class Config():
    SECRET_KEY = "secret key"
    JWT_SECRET_KEY="jwt secret key"
    JWT_ACCESS_TOKEN_EXPIRE = timedelta(hours=12)

# DATABASE

    SQLALCHEMY_DATABASE_URI = "sqlite:///"+ os.path.join(INSTANCE , "database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# REDIS

    REDIS_URL = "redis://localhost:6379/0"
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = REDIS_URL
    CACHE_DEFAULT_TIMEOUT = 300

#CELERY

    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"

    Export = os.path.join(INSTANCE , "export")
    Upload = os.path.join(INSTANCE , "upload")

os.makedirs(Config.Export, exist_ok=True)
os.makedirs(Config.Upload, exist_ok=True)   