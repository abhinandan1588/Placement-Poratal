from flask import Flask , jsonify 
from extensions import db, jwt , cache , cors
from models import User , StudentProfile , CompanyProfile , PlacementDrive , Application
from config import Config
from resources import register_blueprints

def _configure_cache(app):
    try:
        import redis

        client = redis.Redis.from_url("redis://localhost:6379/0", socket_connect_timeout=1)
        client.ping()
        app.config["CACHE_TYPE"] = "RedisCache"
        app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/0"

        print("cache is connected to the redis")
    except:
        app.config["CACHE_TYPE"] = "SimpleCache"
        print("Redis unavailable , using in-memory- simple cache")
    cache.init_app(app)


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app , resources={r"/api/*":{"origins":"*"}})
    _configure_cache(app)
    register_blueprints(app)

    with app.app_context():
        db.create_all()
        if not User.query.filter_by(role = "admin").first():
            admin = User(email = "admin@ppa.com" , role = "admin")
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)