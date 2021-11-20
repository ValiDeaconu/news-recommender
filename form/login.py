from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.fields.core import IntegerField
from wtforms.fields.simple import TextField

class Form(FlaskForm):
    username = TextField('username')
    password = TextField('password')