from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import render_template


class MyView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_parent

    def inaccessible_callback(self, name, **kwargs):
        return render_template('403.html')

    def is_visible(self):
        return current_user.is_authenticated and current_user.is_parent


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_parent

    def inaccessible_callback(self, name, **kwargs):
        return render_template('403.html')

    def is_visible(self):
        return current_user.is_authenticated and current_user.is_parent




