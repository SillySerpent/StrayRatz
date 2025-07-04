import os
from datetime import timedelta

class Config:
    # Secret key for forms and secure sessions
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Database configuration
    base_dir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{os.path.join(base_dir, "instance", "site.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session lifetime (reduced for security)
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    
    # Admin account defaults - should be changed in production
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')  # Will be used only for initial setup 

    # Mail settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # Email verification settings
    EMAIL_VERIFICATION_REQUIRED = os.environ.get('EMAIL_VERIFICATION_REQUIRED', 'False').lower() == 'true'

class DevelopmentConfig(Config):
    DEBUG = True
    # Disable email verification in development mode
    EMAIL_VERIFICATION_REQUIRED = False