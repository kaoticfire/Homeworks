from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import timedelta

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True, duration=timedelta(hours=24))
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template('login.html', user=current_user)


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
                flash('Email must be greater than 4 characters.', category='error')
            elif password1 != password2:
                flash('Passwords do not match.', category='warning')
            elif len(password1) < 8:
                flash('Password must be greater than 7 characters.', category='error')
            else:
                user.password = generate_password_hash(password1, method='sha256')
                db.session.commit()
                flash('Password has been successfully reset', category='success')
                return redirect(url_for('views.home'))

    return render_template('reset_request.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 5:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(first_name) < 3:
            flash('Firstname must be greater than 2 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='warning')
        elif len(password1) < 8:
            flash('Password must be greater than 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)
