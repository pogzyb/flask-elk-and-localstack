from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from app.models import User


class RegisterUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_repeat = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username_exists(self, username: str):
        exists = User.query().filter_by(username=username).first()
        if exists:
            raise ValidationError('That username already exists!')

    def validate_email_exists(self, email: str):
        exists = User.query().filter_by(email=email).first()
        if exists:
            raise ValidationError('That email address is already in use!')


class LoginUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email('Please enter a valid email address')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email('Please enter a valid email address')])
    submit = SubmitField('Login')
