from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                          validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                       validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
            
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                       validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class NewsletterForm(FlaskForm):
    name = StringField('Name (Optional)', validators=[Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Subscribe')

class SurveyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    current_supplements = SelectField('What supplements do you currently use?',
                                    choices=[
                                        ('none', 'None'),
                                        ('preworkout', 'Pre-workout'),
                                        ('protein', 'Protein'),
                                        ('bcaa', 'BCAAs'),
                                        ('creatine', 'Creatine'),
                                        ('multiple', 'Multiple supplements'),
                                        ('other', 'Other')
                                    ])
    
    interest_level = RadioField('How interested are you in an all-in-one supplement solution?',
                              choices=[
                                  ('1', 'Not interested'),
                                  ('2', 'Slightly interested'),
                                  ('3', 'Moderately interested'),
                                  ('4', 'Very interested'),
                                  ('5', 'Extremely interested')
                              ], validators=[DataRequired()])
    
    price_preference = SelectField('What price range would you consider reasonable for our all-in-one supplement?',
                                 choices=[
                                     ('under30', 'Under $30'),
                                     ('30to40', '$30-$40'),
                                     ('40to50', '$40-$50'),
                                     ('50to60', '$50-$60'),
                                     ('over60', 'Over $60')
                                 ])
    
    heard_from = RadioField('How did you hear about StrayRatz?',
                          choices=[
                              ('social', 'Social Media'),
                              ('friend', 'Friend or Family'),
                              ('search', 'Search Engine'),
                              ('ad', 'Online Advertisement'),
                              ('other', 'Other')
                          ])
    
    additional_comments = TextAreaField('Additional Comments')
    
    submit = SubmitField('Submit Survey') 