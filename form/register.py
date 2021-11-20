from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.widgets import PasswordInput
from wtforms.validators import DataRequired, Length, EqualTo

FIELD_REQUIRED_TPL = 'Campul "{}" este obligatoriu.'
MINIMUM_LENGTH_TPL = 'Campul "{}" trebuie sa contina minim {} caractere.'

class Form(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(message=FIELD_REQUIRED_TPL.format('nume de utilizator')), 
        Length(min=6, message=MINIMUM_LENGTH_TPL.format('nume de utilizator', '6'))
    ])
    password = StringField('password', widget=PasswordInput(hide_value=False), validators=[
        DataRequired(message=FIELD_REQUIRED_TPL.format('parola')), 
        Length(min=8, message=MINIMUM_LENGTH_TPL.format('parola', '8'))
    ])
    confirm_password = StringField('confirm_password', widget=PasswordInput(hide_value=False), validators=[
        DataRequired(message=FIELD_REQUIRED_TPL.format('parola')), 
        Length(min=8, message=MINIMUM_LENGTH_TPL.format('parola', '8')),
        EqualTo('password', message='Parolele nu coincid.')
    ])