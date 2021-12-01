""" Custom error pages for the flask application. """

from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_four_o_four(error):
    """ Custom page not found error. """
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_four_o_three(error):
    """ Custom permission denied error. """
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_five_hundred(error):
    """ Custom internal server error. """
    return render_template('errors/500.html'), 500
