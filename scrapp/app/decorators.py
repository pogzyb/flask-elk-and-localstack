from functools import wraps

from flask_login import current_user
from flask import url_for, redirect, flash
from structlog import get_logger

logger = get_logger(__name__)


class GenericAuthMessages:
    login_needed_info = ('Please log in to perform that action.', 'info')
    no_auth_warning = ('Oops! You\'re not authorized to perform that action.', 'warning')


def api_role_required(*role_names):

    def wrapper(view_function):
        return

    return


def roles_required(*role_names):
    """
    Ensures that the current user is logged in and has *all* of the specified roles (AND operation).

    Example::
        @route('/escape')
        @roles_required('Special', 'Agent')
        def escape_capture():  # User must be 'Special' AND 'Agent'
            ...
    """
    def wrapper(view_function):

        @wraps(view_function)    # Tells debuggers that is is a function wrapper
        def decorator(*args, **kwargs):
            if not current_user.is_authenticated:
                flash(*GenericAuthMessages.login_needed_info)
                return redirect('/login')

            if not current_user.has_all_roles(*role_names):
                # Redirect to the unauthorized page
                flash(*GenericAuthMessages.no_auth_warning)
                return redirect('/')

            # It's OK to call the view
            return view_function(*args, **kwargs)
        return decorator

    return wrapper
