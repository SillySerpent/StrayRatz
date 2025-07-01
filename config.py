import os
from datetime import timedelta

class Config:
    # Secret key for forms and secure sessions
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jsdaglwbuh4piugeirablgjk4/twt/3t;j3glre48o;r4j43tj/er;gwpu'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session lifetime
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Admin account defaults - should be changed in production
    ADMIN_USERNAME = "juju"
    ADMIN_EMAIL = 'Josephayleshaa@gmail.com'
    ADMIN_PASSWORD = 'BlackwizzerdBlackwizzerdBlackwizzerd'  # Will be used only for initial setup 

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'Josephayleshaa@gmail.com'
    MAIL_PASSWORD = 'BlackwizzerdBlackwizzerdBlackwizzerd'
    MAIL_DEFAULT_SENDER = 'Josephayleshaa@gmail.com'