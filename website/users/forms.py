""" All custom forms pertaining to the Users package. """

from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from website.models import User


class RegistrationForm(FlaskForm):
    """ A custom signup form. """
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    @staticmethod
    def validate_username(first_name):
        """ Function to ensure valid data is put in to be submitted.

        ARGS:
            first_name: the first name of the new user.

        Rasis:
            ValidationError: raises a exception if empty or invalid characters are placed in the form. """
        user = User.query.filter_by(first_name=first_name.data).first()
        if user:
            raise ValidationError('That username is taken. Please try a different one.')

    @staticmethod
    def validate_email(email):
        """ Function to ensure valid data is put in to be submitted.

        ARGS:
            email: the email address of the new user.

        Rasis:
            ValidationError: raises a exception if empty or invalid characters are placed in the form. """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please try a different one.')


class LoginForm(FlaskForm):
    """ a custom login form. """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """ A custom account update form. """
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    @staticmethod
    def validate_username(first_name):
        """ Function to ensure valid data is put in to be submitted.

        ARGS:
            first_name: the first name of the cerrent user.

        Rasis:
            ValidationError: raises a exception if empty or invalid characters are placed in the form. """
        if first_name.data != current_user.first_name:
            user = User.query.filter_by(username=first_name.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    @staticmethod
    def validate_email(email):
        """ Function to ensure valid data is put in to be submitted.

        ARGS:
            email: the email address of the current user.

        Rasis:
            ValidationError: raises a exception if empty or invalid characters are placed in the form. """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    """ A custom form to request a password reset. """
    email = StringField('Email', alidators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    @staticmethod
    def validate_email(email):
        """ Function to ensure valid data is put in to be submitted.

        ARGS:
            email: the email address of the current user.

        Rasis:
            ValidationError: raises a exception if empty or invalid characters are placed in the form. """
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No account with that email found.')


class ResetPasswordForm(FlaskForm):
    """ A custom form for a user to update their password, once a valid security token is provided. """
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Password Reset')
