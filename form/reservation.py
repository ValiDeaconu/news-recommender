from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.fields.core import IntegerField
from wtforms.fields.simple import TextField

class Form(FlaskForm):
    name = TextField('name')
    county = SelectField('county', choices=[])
    locality = SelectField('locality', choices=[])
    age = IntegerField('age')
    row = SelectField('row', choices=[])
    column = SelectField('column', choices=[])
    day = SelectField('day', choices=[])
    movie = SelectField('movie', choices=[])