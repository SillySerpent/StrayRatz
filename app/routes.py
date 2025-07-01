from flask import Blueprint, render_template, url_for, flash, redirect, request, jsonify, current_app
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash

from app import db
from app.models import User, NewsletterSubscriber, Survey
from app.forms import RegistrationForm, LoginForm, NewsletterForm, SurveyForm
from config import Config

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def index():
    from datetime import datetime
    newsletter_form = NewsletterForm()
    now = datetime.now()
    return render_template('index.html', title='StrayRatz - All-In-One Supplement', form=newsletter_form, now=now)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if user.is_admin:
                return redirect(next_page or url_for('admin.dashboard'))
            return redirect(next_page or url_for('main.index'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/survey', methods=['GET', 'POST'])
def survey():
    form = SurveyForm()
    if form.validate_on_submit():
        survey = Survey(
            email=form.email.data,
            name=form.name.data,
            current_supplements=form.current_supplements.data,
            interest_level=int(form.interest_level.data),
            price_preference=form.price_preference.data,
            heard_from=form.heard_from.data,
            additional_comments=form.additional_comments.data
        )
        if current_user.is_authenticated:
            survey.user_id = current_user.id
            
        db.session.add(survey)
        db.session.commit()
        flash('Thank you for completing our survey!', 'success')
        return redirect(url_for('main.thank_you'))
    return render_template('survey.html', title='Product Survey', form=form)

@main.route('/thank-you')
def thank_you():
    return render_template('thank_you.html', title='Thank You')

@main.route('/api/subscribe', methods=['POST'])
def newsletter_subscribe():
    form = NewsletterForm()
    print("Newsletter subscription attempt:", request.form)
    if form.validate_on_submit():
        # Check if email already exists
        existing = NewsletterSubscriber.query.filter_by(email=form.email.data).first()
        if existing:
            return jsonify({'success': False, 'message': 'Email already subscribed'})
            
        subscriber = NewsletterSubscriber(
            email=form.email.data,
            name=form.name.data if form.name.data else None
        )
        db.session.add(subscriber)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Successfully subscribed to newsletter'})
    return jsonify({'success': False, 'message': 'Invalid form data'})

@main.route('/privacy-policy')
def privacy_policy():
    from datetime import datetime
    now = datetime.now()
    return render_template('privacy_policy.html', title='Privacy Policy', config=Config, now=now)

@main.route('/terms-of-service')
def terms_of_service():
    from datetime import datetime
    now = datetime.now()
    return render_template('terms_of_service.html', title='Terms of Service', config=Config, now=now)

@main.route('/about')
def about():
    from datetime import datetime
    now = datetime.now()
    return render_template('about.html', title='About StrayRatz', now=now) 