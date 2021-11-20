from flask_wtf import FlaskForm
from wtforms.fields.simple import TextField

class Form(FlaskForm):
    username = TextField('username')
    password = TextField('password')
    confirm_password = TextField('confirm_password')