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

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Sorry - that username is taken!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('That email address is already in use!')


class LoginUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email('Please enter a valid email address')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class StartResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email('Please enter a valid email address')])
    submit = SubmitField('Send Password Reset Instructions')


class CompleteResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    password_repeat = PasswordField('Repeat New Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update Password')
