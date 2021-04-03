from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from app.blueprints.auth.models import User


class SignUpUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_repeat = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')
    # remember_me =

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Oops. That email address is already in use.')


class LoginUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email('Please enter a valid email address')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class StartResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email('Please enter a valid email address')])
    submit = SubmitField('Send Account Recovery Instructions')


class CompleteResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    password_repeat = PasswordField('Repeat New Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update Password')
