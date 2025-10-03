import os
from flask import Flask
from dotenv import load_dotenv
from config import DevelopmentConfig, ProductionConfig
from extensions import db, login_manager, migrate
from datetime import datetime  # <-- IMPORT THE DATETIME MODULE

# Load environment variables from .env file
load_dotenv()

def create_app():
    """
    Factory function to create and configure the Flask application.
    """
    app = Flask(__name__)

    # Determine which configuration to use based on FLASK_ENV
    config_class = ProductionConfig if os.environ.get('FLASK_ENV') == 'production' else DevelopmentConfig
    app.config.from_object(config_class)

    # Initialize extensions with the application instance
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Configure Flask-Login settings
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # Import models to ensure they are registered with SQLAlchemy
    from models import User

    # User loader function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
        
    # NEW: Context processor to inject variables into all templates
    @app.context_processor
    def inject_now():
        """Injects the current UTC date and time into all templates."""
        return {'now': datetime.utcnow}

    # Register Blueprints for different parts of the app
    from routes.portfolio import portfolio_bp
    from routes.admin import admin_bp
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    with app.app_context():
        # Create database tables for our models if they don't exist
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    # Use the PORT environment variable for deployment, default to 5000 for local dev
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
