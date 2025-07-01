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

class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[Length(max=64)])
    last_name = StringField('Last Name', validators=[Length(max=64)])
    bio = TextAreaField('About Me', validators=[Length(max=500)])
    location = StringField('Location', validators=[Length(max=128)])
    fitness_goals = StringField('Fitness Goals', validators=[Length(max=128)])
    fitness_level = SelectField('Fitness Level', 
                              choices=[
                                  ('beginner', 'Beginner'),
                                  ('intermediate', 'Intermediate'),
                                  ('advanced', 'Advanced'),
                                  ('professional', 'Professional/Athlete')
                              ])
    submit = SubmitField('Update Profile')

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
    
    # Enhanced rating fields
    effectiveness_rating = RadioField('How important is effectiveness to you when choosing supplements?',
                                   choices=[
                                       ('1', 'Not important'),
                                       ('2', 'Slightly important'),
                                       ('3', 'Moderately important'),
                                       ('4', 'Very important'),
                                       ('5', 'Extremely important')
                                   ], validators=[DataRequired()])
    
    value_rating = RadioField('How important is value for money when choosing supplements?',
                           choices=[
                               ('1', 'Not important'),
                               ('2', 'Slightly important'),
                               ('3', 'Moderately important'),
                               ('4', 'Very important'),
                               ('5', 'Extremely important')
                           ], validators=[DataRequired()])
    
    convenience_rating = RadioField('How important is convenience when choosing supplements?',
                                 choices=[
                                     ('1', 'Not important'),
                                     ('2', 'Slightly important'),
                                     ('3', 'Moderately important'),
                                     ('4', 'Very important'),
                                     ('5', 'Extremely important')
                                 ], validators=[DataRequired()])
    
    price_preference = SelectField('What price range would you consider reasonable for our all-in-one supplement?',
                                 choices=[
                                     ('under30', 'Under $30'),
                                     ('30to40', '$30-$40'),
                                     ('40to50', '$40-$50'),
                                     ('50to60', '$50-$60'),
                                     ('over60', 'Over $60')
                                 ])
    
    specific_needs = TextAreaField('What specific needs are you looking to address with supplements?',
                                validators=[Length(max=500)])
                                
    pain_points = TextAreaField('What frustrates you most about current supplement options?',
                             validators=[Length(max=500)])
                             
    expected_benefits = TextAreaField('What benefits would you expect from an all-in-one supplement?',
                                   validators=[Length(max=500)])
    
    purchase_likelihood = RadioField('How likely would you be to purchase our all-in-one supplement?',
                                  choices=[
                                      ('1', 'Very unlikely'),
                                      ('2', 'Somewhat unlikely'),
                                      ('3', 'Neutral'),
                                      ('4', 'Somewhat likely'),
                                      ('5', 'Very likely')
                                  ], validators=[DataRequired()])
    
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