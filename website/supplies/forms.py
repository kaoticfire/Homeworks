from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SupplyForm(FlaskForm):
    supply = StringField('Item', validators=[DataRequired()])
    submit = SubmitField('Submit')
