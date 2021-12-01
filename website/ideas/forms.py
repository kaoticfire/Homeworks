""" Custom new dinner idea form. """

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired


class IdeaForm(FlaskForm):
    """ Form contains a title and a recipe url. """
    title = StringField('Idea', validators=[DataRequired()])
    recipe = URLField('URL')
    submit = SubmitField('Submit')
