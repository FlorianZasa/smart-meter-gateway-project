from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from config import Config

bcrypt = Bcrypt()
jwt = JWTManager()
db = None

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)
    jwt.init_app(app)

    global db
    client = MongoClient(app.config['MONGO_URI'])
    db = client.get_database('smg')

    # Importiere Blueprints
    from app.auth.routes import bp as auth_bp
    from app.main.routes import bp as main_bp

    # Registrieres blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp, url_prefix='/main')

    return app