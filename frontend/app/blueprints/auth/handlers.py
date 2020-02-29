import logging

from flask_login import (
    current_user,
    login_user,
    logout_user
)
from flask import (
    redirect,
    url_for,
    render_template,
    request,
    flash
)

from app.models import User
from app import db
from app.blueprints.auth import auth
from app.blueprints.auth.email import me
from app.blueprints.auth.forms import (
    RegisterUserForm,
    LoginUserForm,
    StartResetPasswordForm,
    CompleteResetPasswordForm
)


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
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('web.index'))
    form = LoginUserForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            existing_user = User.query.filter_by(email=form.email.data).first()
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


@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('web.index'))
    form = StartResetPasswordForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                token = user.get_reset_password_token()
                me.send_password_reset_email(user.email, token)
            flash('Sending instructions to that email address!', 'success')
            return redirect(url_for('auth.reset_password'))
    return render_template('auth/reset_start.html', form=form)


@auth.route('/reset_password/<string:token>', methods=['GET', 'POST'])
def reset_password_with_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('web.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        flash('That token is invalid!', 'danger')
        return redirect(url_for('web.index'))
    form = CompleteResetPasswordForm(request.form)
    if form.validate_on_submit():
        user.set_password_hash(form.password.data)
        db.session.commit()
        flash('Your password was successfully updated!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_complete.html', form=form)
