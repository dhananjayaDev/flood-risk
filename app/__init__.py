from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()

def create_app():
    import os
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        # Create tables for kalugangadb
        try:
            # Import the RiverHeight model to ensure it's registered
            from app.models import RiverHeight
            # Create the table for the kalugangadb bind
            RiverHeight.__table__.create(db.engines['kalugangadb'], checkfirst=True)
        except Exception as e:
            print(f"Note: Could not create kalugangadb tables: {e}")
    
    # Start automatic river data collection scheduler
    try:
        from app.scheduler import start_automatic_collection
        if start_automatic_collection():
            print("✅ Automatic river data collection started")
        else:
            print("⚠️ Failed to start automatic data collection")
    except Exception as e:
        print(f"⚠️ Scheduler not available: {e}")
    
    return app
