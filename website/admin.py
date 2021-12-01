""" Custom administrative views. """
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import render_template


class MyView(ModelView):
    """ Custom database view inside the admin view. """
    def is_accessible(self):
        """ Flag for if the admin view is accessible. """
        return current_user.is_authenticated and current_user.is_parent

    def inaccessible_callback(self, name, **kwargs):
        """ Error page user is sent to if they are not authorized to access the admin section. """
        return render_template('errors/403.html')

    def is_visible(self):
        """ flag to determine whether the admin section can be seen by all. """
        return current_user.is_authenticated and current_user.is_parent


class MyAdminIndexView(AdminIndexView):
    """ Custom admin interface view. """
    def is_accessible(self):
        """ Flag for if the admin view is accessible. """
        return current_user.is_authenticated and current_user.is_parent

    def inaccessible_callback(self, name, **kwargs):
        """ Error page user is sent to if they are not authorized to access the admin section. """
        return render_template('errors/403.html')

    def is_visible(self):
        """ flag to determine whether the admin section can be seen by all. """
        return current_user.is_authenticated and current_user.is_parent
