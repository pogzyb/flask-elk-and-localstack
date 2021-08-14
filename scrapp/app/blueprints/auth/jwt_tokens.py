import jwt
from flask import session
from werkzeug.wrappers import Request, Response, ResponseStream

from app.cache import get_token, put_token
from .models import User


class JWTAuthMiddleware:

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response, *args, **kwargs):

        return

    def get_current_user(self):
        # decode the token and see if it's valid
        # try to retrieve it from redis session cache
        # load the user and save into request context

        return

    def check_token(self):

        return


class JWTLoginManager:
    """
    Simple JWT Manager; created for learning purposes
    """

    def __init__(self):
        ...

    def login_user(self, user: User, remember=True):

        access_token = user.generate_token(key='user', expires=600)
        refresh_token = user.generate_token(key='user', expires=1800)

        session['access_token'] = user.generate_token(key='user_id', expires=600)
        session['refresh_token'] = user.generate_token(key='user_id', expires=1800)
