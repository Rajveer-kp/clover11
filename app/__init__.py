from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import environ

# Import your extensions and blueprints
from app.models.user import db  # SQLAlchemy instance
from app.routes.auth import auth
from app.routes.views import views
from app.routes.youtube_auth import youtube_bp


def create_app():
    # Load environment variables from .env file
    load_dotenv()

    # Create Flask app
    app = Flask(__name__)

    # Basic Configurations
    app.secret_key = 'simple-production-key-2025'
    
    # Database configuration for Vercel (serverless environment)
    database_url = environ.get('DATABASE_URL')
    if database_url:
        # Production: Use external database (PostgreSQL, etc.)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Development fallback: Use in-memory SQLite for Vercel compatibility
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
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

    # Create database tables only if we have a database
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            # Log the error but don't crash the app
            print(f"Database initialization warning: {e}")

    return app
