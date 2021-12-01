""" Custom new supply need form. """
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SupplyForm(FlaskForm):
    """ form containing one text field and a submit button. """
    supply = StringField('Item', validators=[DataRequired()])
    submit = SubmitField('Submit')
