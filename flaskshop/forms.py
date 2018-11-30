from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskshop.models import User

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max = 25)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=8, max= 16)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Account already created with this email address.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class FavouriteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Create Board')

class FavClickForm(FlaskForm):
    submit = SubmitField('Choose Board')
