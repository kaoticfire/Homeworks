from flask import Blueprint, render_template, flash, redirect, url_for
from website.models import User
from pass_util.forms import AdminResetPasswordForm
from website import db
from werkzeug.security import generate_password_hash
from flask_login import current_user

passwd = Blueprint('passwd', __name__)


@passwd.route("/password_reset", methods=["GET", "POST"])
def reset():
    if not current_user.is_authenticated:
        return redirect(url_for("users.login"))
    form = AdminResetPasswordForm()
    user = User.query.filter_by(first_name=str(form.user.data))
    if user is None:
        flash("No such user found.", "warning")
        return redirect(url_for("pass_util.reset"))
    if form.validate_on_submit():
        user.password = generate_password_hash(form.password.data, method="sha256")
        db.session.commit()
        flash("The password has been updated!", "success")
        return redirect(url_for("messages.message"))
    return render_template("pass_reset.html", form=form)
