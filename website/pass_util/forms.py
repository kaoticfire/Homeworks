from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from wtforms_sqlalchemy.fields import QuerySelectField
from website.models import User


def get_user_info():
    user = User.query
    return user


class AdminResetPasswordForm(FlaskForm):
    user = QuerySelectField('Recipient',
                            validators=[DataRequired()],
                            query_factory=get_user_info,
                            get_label='first_name')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
