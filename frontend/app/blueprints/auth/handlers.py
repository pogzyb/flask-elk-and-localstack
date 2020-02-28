import logging

from flask_mail import Message
from flask_login import current_user, login_user, logout_user
from flask import redirect, url_for, render_template, request, flash

from app.blueprints.auth import auth
from app.blueprints.auth.email import me
from app.blueprints.auth.forms import RegisterUserForm, LoginUserForm
from app.models import User
from app import db, mail


logger = logging.getLogger(__name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('web.index'))
    form = RegisterUserForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(username=form.username.data, email=form.email.data)
            new_user.set_password_hash(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration Complete - Welcome!', 'success')
            return redirect(url_for('web.index'))
    else:
        return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('web.index'))
    form = LoginUserForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            existing_user = User.query.filter_by(email=form.email.data).first()
            logger.info(f'GOT USER: {existing_user}')
            if not existing_user or not existing_user.check_password(form.password.data):
                flash('Invalid username/password combination!', 'danger')
                return redirect(url_for('auth.login'))
            else:
                login_user(existing_user)
                return redirect(url_for('web.index'))
    else:
        return render_template('auth/login.html', form=form)


@auth.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('web.index'))


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    # me.send_password_reset_email('cheese')
    send_email("Hi!", "foo@bar.com", ["pogzyb@umich.edu"], "HELLO", "<p>Hello this is a test</p>")
    # if current_user.is_authenticated:
    #     return redirect(url_for('web.index'))
    # if request.method == 'POST':
    #     form = request.form
    #     email_exists = User.query.filter_by(email=form.email.data).first()
    #     if email_exists:
    #         me.send_password_reset_email()
    #
    # else:
    return redirect(url_for('auth.register'))
