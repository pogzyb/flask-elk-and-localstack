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
from app import db, mail
from app.blueprints.auth import auth
from app.blueprints.auth.forms import (
    SignUpUserForm,
    LoginUserForm,
    StartResetPasswordForm,
    CompleteResetPasswordForm
)


logger = logging.getLogger(__name__)


class AuthFlashMessages:

    start_verify_account    = ('Welcome! Check your email to verify your account.', 'info'),
    end_verify_account      = ('Awesome! Your account is now verified and you\'re all set.', 'success'),
    invalid_user            = ('Uh oh! The email or password you entered wasn\'t valid.', 'danger'),
    start_reset_password    = ('Sending reset instructions to that email address!', 'info'),
    end_reset_password      = ('Success! Your password was updated.', 'success'),
    resend_verify_account   = ('Success! Re-sent the verification email.', 'success'),
    expired_token           = ('Oops! That token expired. Try again.', 'warning'),
    invalid_token           = ('The token you provided was not valid.', 'info')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('web.index'))
    form = SignUpUserForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            # create user and save to db
            new_user = User(email=form.email.data)
            new_user.password = form.password.data
            db.session.add(new_user)
            db.session.commit()
            # generate token for the verification email
            token = new_user.generate_token('verification', expires=300)
            # send verification email
            mail.send_verification_email(new_user.email, token)
            flash(*AuthFlashMessages.start_verify_account)
            return redirect(url_for('web.index'))
        else:
            logger.info(f'form posted to "/signup" was invalid')
            return render_template('auth/signup.html', form=form)

    return render_template('auth/signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('web.index'))
    form = LoginUserForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            existing_user = User.query.filter_by(email=form.email.data).first()
            if not existing_user or not existing_user.check_password(form.password.data):
                flash(*AuthFlashMessages.invalid_user)
                return redirect(url_for('auth.login'))
            else:
                login_user(existing_user)
                return redirect(url_for('web.index'))

    return render_template('auth/login.html', form=form)


@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('web.index'))
    form = StartResetPasswordForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                token = user.generate_token("reset", expires=300)
                mail.send_password_reset_email(user.email, token)
            flash(*AuthFlashMessages.start_reset_password)
            return redirect(url_for('auth.reset_password'))
    return render_template('auth/reset_start.html', form=form)


@auth.route('/reset-password/<string:token>', methods=['GET', 'POST'])
def reset_password_with_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('web.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        flash(*AuthFlashMessages.expired_token)
        return redirect(url_for('web.index'))
    form = CompleteResetPasswordForm(request.form)
    if form.validate_on_submit():
        user.set_password_hash(form.password.data)
        db.session.commit()
        flash(*AuthFlashMessages.end_reset_password)
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_complete.html', form=form)


@auth.route('/verify-account', methods=['GET'])
def verify_account():
    token = request.args.get('token')
    if not token:
        flash(*AuthFlashMessages.invalid_token)
        return redirect(url_for('web.index'))
    else:
        return


@auth.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('web.index'))
