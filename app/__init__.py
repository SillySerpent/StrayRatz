from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import Config
import os
import json
from werkzeug.security import generate_password_hash

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_class=None):
    app = Flask(__name__)

    if config_class:
        app.config.from_object(config_class)
    else:
        from config import Config
        app.config.from_object(Config)

    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
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
    
    # Register blueprints
    from app.routes import main
    from app.admin import admin
    
    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin')
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create default admin if no users exist
        from app.models import User
        admin_user = User.query.filter_by(username='juju').first()
        if not admin_user:
            admin_user = User(
                username='juju',
                email='admin@strayratz.com',
                is_admin=True
            )
            
            # Set default password
            default_password = 'BlackwizzerdBlackwizzerdBlackwizzerd'
            admin_user.password_hash = generate_password_hash(default_password)
            
            db.session.add(admin_user)
            db.session.commit()
            
            print(f"Default admin created: {admin_user.username}")
            print(f"Default admin password: {default_password}")
            print("Please change this password after first login!")
    
    return app 