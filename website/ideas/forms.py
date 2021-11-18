from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired


class IdeaForm(FlaskForm):
    title = StringField('Idea', validators=[DataRequired()])
    recipe = URLField('URL')
    submit = SubmitField('Submit')
