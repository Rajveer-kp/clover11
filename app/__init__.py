from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import environ

# Import your extensions and blueprints
from app.models.user import db  # SQLAlchemy instance
from app.routes.auth import auth
from app.routes.views import views
from app.routes.youtube_auth import youtube_bp
from app.adsense_config import get_adsense_script_tag, get_ad_unit, get_auto_ads_script, ADSENSE_CONFIG

def create_app():
    # Load environment variables from .env file
    load_dotenv()

    # Create Flask app
    app = Flask(__name__)

    # Basic Configurations
    app.secret_key = environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL', 'sqlite:///site.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ENV'] = environ.get('FLASK_ENV', 'development')

    # Initialize database with app
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(youtube_bp, url_prefix='/youtube')

    # Import models to ensure they're created
    from app.models.user import User
    from app.models.pending_video import PendingVideo
    from app.models.invitation import Invitation
    from app.models.advertisement import Advertisement, AdClick

    # Add AdSense helper to template context
    @app.context_processor
    def inject_adsense():
        return {
            'adsense_script': get_adsense_script_tag(),
            'adsense_auto_ads': get_auto_ads_script(),
            'get_ad_unit': get_ad_unit,
            'adsense_config': ADSENSE_CONFIG
        }

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
