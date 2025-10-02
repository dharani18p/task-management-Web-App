from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
cache = Cache()
migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    
    from config import Config
    app.config.from_object(Config)

    # 👇 This is the new line you need to add
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.routes import api_bp
    from app.pages import pages_bp
    app.register_blueprint(api_bp, url_prefix='/api')  # API routes prefixed with /api
    app.register_blueprint(pages_bp)                  # HTML pages without prefix
    
    return app