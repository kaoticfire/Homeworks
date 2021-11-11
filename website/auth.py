from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from .forms import LoginForm, RegistrationForm
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import timedelta

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data, duration=timedelta(hours=24))
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('views.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'error')
    return render_template('login.html', title='Login', form=form, user=current_user)


@auth.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    # TODO: Add password reset capabilities.
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            if len(email) < 5:
                flash('Email must be greater than 4 characters.', 'error')
            elif password1 != password2:
                flash('Passwords do not match.', 'warning')
            elif len(password1) < 8:
                flash('Password must be greater than 7 characters.', 'error')
            else:
                user.password = generate_password_hash(password1, method='sha256')
                db.session.commit()
                flash('Password has been successfully reset', 'success')
                return redirect(url_for('views.home'))

    return render_template('reset_request.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, email=form.email.data,
                    password=generate_password_hash(form.password.data, method='sha256'))
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('sign_up.html', title='Register', form=form, user=current_user)
