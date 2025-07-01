from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.routes import main
    from app.admin import admin
    
    app.register_blueprint(main)
    app.register_blueprint(admin)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create default admin if no users exist
        from app.models import User
        if not User.query.filter_by(is_admin=True).first():
            from werkzeug.security import generate_password_hash
            default_admin = User(
                username=app.config['ADMIN_USERNAME'],
                email=app.config['ADMIN_EMAIL'],
                password_hash=generate_password_hash(app.config['ADMIN_PASSWORD']),
                is_admin=True
            )
            db.session.add(default_admin)
            db.session.commit()
            print(f"Default admin created: {app.config['ADMIN_USERNAME']}")
            print(f"Default admin password: {app.config['ADMIN_PASSWORD']}")
            print("Please change this password after first login!")
    
    return app 