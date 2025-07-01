from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login_manager

# User loader moved to __init__.py

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Profile fields
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(128), nullable=True)
    fitness_goals = db.Column(db.String(128), nullable=True)
    fitness_level = db.Column(db.String(32), nullable=True)
    
    surveys = db.relationship('Survey', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class NewsletterSubscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=True)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<NewsletterSubscriber {self.email}>'

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    email = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    current_supplements = db.Column(db.Text, nullable=True)
    interest_level = db.Column(db.Integer, nullable=False)
    price_preference = db.Column(db.String(64), nullable=True)
    heard_from = db.Column(db.String(64), nullable=True)
    
    # Enhanced survey fields
    effectiveness_rating = db.Column(db.Integer, nullable=True)
    value_rating = db.Column(db.Integer, nullable=True)
    convenience_rating = db.Column(db.Integer, nullable=True)
    specific_needs = db.Column(db.Text, nullable=True)
    pain_points = db.Column(db.Text, nullable=True)
    expected_benefits = db.Column(db.Text, nullable=True)
    purchase_likelihood = db.Column(db.Integer, nullable=True)
    
    additional_comments = db.Column(db.Text, nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Survey {self.id} by {self.email}>' 