from flask_sqlalchemy import SQLAlchemy # for database 
from flask_jwt_extended import JWTManager # for token authentication 
from flask_caching import Cache # for catching 
from flask_cors import CORS # for making the connection between backend and frontend

db = SQLAlchemy()
jwt = JWTManager()
cache = Cache()
cors = CORS()


