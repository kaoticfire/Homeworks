from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired
from website.models import User
from wtforms_sqlalchemy.fields import QuerySelectField


def get_user_info():
    user = User.query
    return user


class MessageForm(FlaskForm):
    recipient = QuerySelectField('Recipient',
                                 validators=[DataRequired()],
                                 query_factory=get_user_info,
                                 get_label='first_name')
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')