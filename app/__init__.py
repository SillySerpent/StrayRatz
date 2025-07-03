from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
import os
import json
import sqlalchemy as sa
from werkzeug.security import generate_password_hash

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'
migrate = Migrate()
csrf = CSRFProtect()
mail = Mail()

def create_app(config_class=None):
    app = Flask(__name__)

    if config_class:
        app.config.from_object(config_class)
    else:
        # Fix the config import
        import sys
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from config import Config
        app.config.from_object(Config)

    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    
    # Define user loader function
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Exempt some routes from CSRF protection
    csrf.exempt('app.routes.newsletter_subscribe')
    
    migrate.init_app(app, db)
    
    # Add custom Jinja filters
    @app.template_filter('from_json')
    def from_json(value):
        try:
            return json.loads(value) if value else []
        except:
            return []
    
    @app.template_filter('type')
    def get_type(value):
        return type(value).__name__
    
    # Register blueprints
    from app.routes import main
    from app.admin import admin
    
    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin')
    
    # Create database tables
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if columns exist and add them if they don't
        inspector = sa.inspect(db.engine)
        if 'user' in inspector.get_table_names():
            columns = [col['name'] for col in inspector.get_columns('user')]
            
            # Add email_confirmed column if not exists
            if 'email_confirmed' not in columns:
                db.engine.execute('ALTER TABLE user ADD COLUMN email_confirmed BOOLEAN DEFAULT FALSE')
            
            # Add email_confirmation_token_created_at column if not exists
            if 'email_confirmation_token_created_at' not in columns:
                db.engine.execute('ALTER TABLE user ADD COLUMN email_confirmation_token_created_at DATETIME')
            
            # Add password_reset_token_created_at column if not exists
            if 'password_reset_token_created_at' not in columns:
                db.engine.execute('ALTER TABLE user ADD COLUMN password_reset_token_created_at DATETIME')
        
        # Create default admin if no users exist
        admin_user = User.query.filter_by(username=app.config.get('ADMIN_USERNAME')).first()
        if not admin_user:
            admin_user = User(
                username=app.config.get('ADMIN_USERNAME', 'admin'),
                email=app.config.get('ADMIN_EMAIL', 'admin@strayratz.com'),
                is_admin=True,
                email_confirmed=True
            )
            
            # Set default password
            default_password = app.config.get('ADMIN_PASSWORD', 'admin')
            admin_user.password_hash = generate_password_hash(default_password)
            
            db.session.add(admin_user)
            db.session.commit()
            
            print(f"Default admin created: {admin_user.username}")
            print(f"Default admin password: {default_password}")
            print("Please change this password after first login!")
    
    return app 